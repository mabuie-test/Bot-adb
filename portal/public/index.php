<?php

declare(strict_types=1);

use App\Controllers\ApiController;
use App\Core\Env;
use App\Core\Router;

require __DIR__ . '/../vendor/autoload.php';
Env::load(dirname(__DIR__));

ini_set('session.cookie_httponly', '1');
ini_set('session.cookie_secure', $_ENV['SESSION_SECURE'] ?? '0');
ini_set('session.use_strict_mode', '1');
header("Content-Security-Policy: default-src 'self'");

$controller = new ApiController();
$router = new Router();
$router->add('GET', '/api/csrf', [$controller, 'csrf']);
$router->add('POST', '/api/account/register', [$controller, 'registerAccount']);
$router->add('POST', '/api/account/login', [$controller, 'loginAccount']);
$router->add('POST', '/api/account/password/request-reset', [$controller, 'requestPasswordReset']);
$router->add('POST', '/api/account/password/reset', [$controller, 'resetPassword']);
$router->add('GET', '/api/account/profile', [$controller, 'profile']);
$router->add('POST', '/api/account/preferences', [$controller, 'updateProfilePreferences']);
$router->add('GET', '/api/account/bets/history', [$controller, 'betHistory']);
$router->add('GET', '/api/account/withdrawals/history', [$controller, 'withdrawalHistory']);
$router->add('POST', '/api/register', [$controller, 'register']);
$router->add('GET', '/api/games', [$controller, 'listGames']);
$router->add('GET', '/api/wallet/balance', [$controller, 'walletBalance']);
$router->add('POST', '/api/deposits/manual', [$controller, 'submitManualDeposit']);
$router->add('GET', '/api/fairness/proof', [$controller, 'fairnessProof']);
$router->add('GET', '/api/round/preview', [$controller, 'roundPreview']);
$router->add('POST', '/api/rounds', [$controller, 'createRound']);
$router->add('GET', '/api/rounds', [$controller, 'listRounds']);
$router->add('GET', '/api/rounds/proof', [$controller, 'roundProof']);
$router->add('POST', '/api/bets', [$controller, 'placeBet']);
$router->add('POST', '/api/bets/cashout', [$controller, 'cashout']);
$router->add('POST', '/api/coinflip/play', [$controller, 'playCoinFlip']);

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$router->dispatch($_SERVER['REQUEST_METHOD'] ?? 'GET', $path);
