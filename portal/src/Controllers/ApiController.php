<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Core\Database;
use App\Core\Response;
use App\Repositories\BetRepository;
use App\Repositories\GameRepository;
use App\Repositories\RoundRepository;
use App\Security\Csrf;
use App\Security\Password;
use App\Security\SeedCrypto;
use App\Services\BetService;
use App\Services\CoinFlipService;
use App\Services\CrashEngine;
use App\Services\PaymentSubmissionService;
use App\Services\ProvablyFairService;
use App\Services\RoundService;
use App\Services\WalletService;

final class ApiController
{
    public function csrf(): void
    {
        Response::json(['csrf_token' => Csrf::token()]);
    }

    public function register(): void
    {
        $data = json_decode((string) file_get_contents('php://input'), true) ?: [];
        $hash = Password::hash((string) ($data['password'] ?? ''));
        Response::json(['message' => 'Registo criado', 'password_hash_example' => $hash], 201);
    }

    public function listGames(): void
    {
        $repo = new GameRepository();
        Response::json(['data' => $repo->listActive()]);
    }

    public function submitManualDeposit(): void
    {
        $data = json_decode((string) file_get_contents('php://input'), true) ?: [];
        if (!Csrf::validate($data['csrf_token'] ?? null)) {
            Response::json(['error' => 'CSRF inválido'], 422);
            return;
        }

        $service = new PaymentSubmissionService();
        $id = $service->submit((int) ($data['user_id'] ?? 0), (string) ($data['reference'] ?? ''), (float) ($data['amount'] ?? 0), (string) ($data['phone'] ?? ''), $data['receipt_url'] ?? null);
        Response::json(['message' => 'Submissão pendente', 'submission_id' => $id], 201);
    }

    public function fairnessProof(): void
    {
        $seed = $_GET['server_seed'] ?? 'seed';
        $client = $_GET['client_seed'] ?? 'client';
        $nonce = (int) ($_GET['nonce'] ?? 1);
        $svc = new ProvablyFairService(new SeedCrypto());
        Response::json($svc->deriveCrashMultiplier((string) $seed, (string) $client, $nonce));
    }

    public function roundPreview(): void
    {
        $game = (string) ($_GET['game'] ?? 'aviator');
        $engine = new CrashEngine(new ProvablyFairService(new SeedCrypto()));
        Response::json($engine->startRound($game));
    }

    public function createRound(): void
    {
        $data = json_decode((string) file_get_contents('php://input'), true) ?: [];
        $game = (string) ($data['game'] ?? 'aviator');
        $gameRepo = new GameRepository();
        $gameRow = $gameRepo->findByShortcode($game);
        if (!$gameRow) {
            Response::json(['error' => 'Jogo não encontrado'], 404);
            return;
        }

        $fair = new ProvablyFairService(new SeedCrypto());
        $engine = new CrashEngine($fair);
        $roundService = new RoundService($engine, $fair, new RoundRepository());
        $round = $roundService->startRound($game, (int) $gameRow['id'], (int) ($data['nonce'] ?? random_int(1, 1000000)), $data['client_seed'] ?? null);
        Response::json(['data' => $round], 201);
    }

    public function placeBet(): void
    {
        $data = json_decode((string) file_get_contents('php://input'), true) ?: [];
        $service = new BetService(new WalletService(), new BetRepository());
        $betId = $service->placeBet((int) $data['round_id'], (int) $data['user_id'], (float) $data['amount'], isset($data['auto_cashout']) ? (float) $data['auto_cashout'] : null);
        Response::json(['message' => 'Aposta criada', 'bet_id' => $betId], 201);
    }

    public function cashout(): void
    {
        $data = json_decode((string) file_get_contents('php://input'), true) ?: [];
        $service = new BetService(new WalletService(), new BetRepository());
        $result = $service->cashout((int) $data['bet_id'], (float) $data['multiplier']);
        Response::json(['message' => 'Cashout efetuado', 'data' => $result]);
    }

    public function listRounds(): void
    {
        $gameId = (int) ($_GET['game_id'] ?? 0);
        if ($gameId <= 0) {
            Response::json(['error' => 'game_id é obrigatório'], 422);
            return;
        }
        $repo = new RoundRepository();
        Response::json(['data' => $repo->latestByGame($gameId)]);
    }


    public function playCoinFlip(): void
    {
        $data = json_decode((string) file_get_contents('php://input'), true) ?: [];
        $service = new CoinFlipService(new ProvablyFairService(new SeedCrypto()), new WalletService());

        try {
            $result = $service->play(
                (int) ($data['user_id'] ?? 0),
                (float) ($data['amount'] ?? 0),
                (string) ($data['choice'] ?? ''),
                $data['client_seed'] ?? null
            );
            Response::json(['message' => 'Coin flip concluído', 'data' => $result], 201);
        } catch (\Throwable $e) {
            Response::json(['error' => $e->getMessage()], 422);
        }
    }

    public function roundProof(): void
    {
        $roundId = (int) ($_GET['round_id'] ?? 0);
        $stmt = Database::connection()->prepare('SELECT round_id, published_hash, revealed_seed, client_seed, nonce, hmac_result, calculation_steps, created_at FROM provably_proofs WHERE round_id=:id LIMIT 1');
        $stmt->execute(['id' => $roundId]);
        $row = $stmt->fetch();
        if (!$row) {
            Response::json(['error' => 'proof não encontrada'], 404);
            return;
        }
        Response::json(['data' => $row]);
    }
}
