<?php
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
while (true) {
    echo 'event: tick' . PHP_EOL;
    echo 'data: ' . json_encode(['time' => microtime(true), 'multiplier' => rand(100, 500) / 100]) . PHP_EOL . PHP_EOL;
    @ob_flush();
    @flush();
    sleep(1);
}
