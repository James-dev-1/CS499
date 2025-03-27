<?php
require_once 'includes/header.php';
require_once 'includes/functions.php';

// Handle scan submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $target = $_POST['target'] ?? '';
    $scan_type = $_POST['scan_type'] ?? '-sS';
    $ports = $_POST['ports'] ?? '';
    $scripts = $_POST['scripts'] ?? '';
    $timing = $_POST['timing'] ?? '3';
    
    $additional_options = [];
    if (!empty($_POST['os_detection'])) $additional_options[] = '-O';
    if (!empty($_POST['aggressive_scan'])) $additional_options[] = '-A';
    if (!empty($_POST['verbose'])) $additional_options[] = '-v';

    $command = build_nmap_command($target, $scan_type, $ports, $scripts, $timing, $additional_options);
    $scan_result = execute_nmap_scan($command);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nmap Scan - Kali Linux Network Tools</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/custom.css" rel="stylesheet">
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar (from index.php) -->
            <nav class="col-md-2 d-md-block bg-dark sidebar">
                <!-- Sidebar content from index.php -->
            </nav>

            <!-- Main Content -->
            <main class="col-md-10 ms-sm-auto px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">Nmap Scan</h1>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Scan Configuration</h5>
                                <form method="POST">
                                    <div class="mb-3">
                                        <label for="target" class="form-label">Target</label>
                                        <input type="text" class="form-control" id="target" name="target" placeholder="IP/Hostname/Range" required>
                                    </div>

                                    <div class="mb-3">
                                        <label class="form-label">Scan Type</label>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="scan_type" id="syn_scan" value="-sS" checked>
                                            <label class="form-check-label" for="syn_scan">TCP SYN Scan</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="scan_type" id="connect_scan" value="-sT">
                                            <label class="form-check-label" for="connect_scan">TCP Connect Scan</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="scan_type" id="udp_scan" value="-sU">
                                            <label class="form-check-label" for="udp_scan">UDP Scan</label>
                                        </div>
                                    </div>

                                    <div class="mb-3">
                                        <label for="ports" class="form-label">Port Range/Specification</label>
                                        <input type="text" class="form-control" id="ports" name="ports" placeholder="e.g., 22,80,443 or 1-1000">
                                    </div>

                                    <div class="mb-3">
                                        <label for="scripts" class="form-label">NSE Scripts</label>
                                        <input type="text" class="form-control" id="scripts" name="scripts" placeholder="e.g., vuln,default">
                                    </div>

                                    <div class="mb-3">
                                        <label for="timing" class="form-label">Timing Template</label>
                                        <select class="form-select" id="timing" name="timing">
                                            <option value="0">T0 - Paranoid</option>
                                            <option value="1">T1 - Sneaky</option>
                                            <option value="2">T2 - Polite</option>
                                            <option value="3" selected>T3 - Normal</option>
                                            <option value="4">T4 - Aggressive</option>
                                            <option value="5">T5 - Insane</option>
                                        </select>
                                    </div>

                                    <div class="mb-3">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="os_detection" name="os_detection">
                                            <label class="form-check-label" for="os_detection">OS Detection</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="aggressive_scan" name="aggressive_scan">
                                            <label class="form-check-label" for="aggressive_scan">Aggressive Scan</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="verbose" name="verbose">
                                            <label class="form-check-label" for="verbose">Verbose Output</label>
                                        </div>
                                    </div>

                                    <button type="submit" class="btn btn-primary">Run Scan</button>
                                </form>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Scan Results</h5>
                                <?php if (isset($scan_result)): ?>
                                    <div class="alert alert-info">
                                        <strong>Command:</strong> <?php echo htmlspecialchars($command); ?>
                                    </div>
                                    <pre><?php echo htmlspecialchars($scan_result); ?></pre>
                                <?php else: ?>
                                    <p class="text-muted">Scan results will appear here after execution.</p>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <script>
        feather.replace();
    </script>
    <script src="assets/js/custom.js"></script>
</body>
</html>
