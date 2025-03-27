<?php
require_once 'includes/header.php';
require_once 'includes/functions.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kali Linux Network Tools</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/custom.css" rel="stylesheet">
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar Navigation -->
            <nav class="col-md-2 d-md-block bg-dark sidebar">
                <div class="position-sticky">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link active" href="nmap_scan.php">
                                <span data-feather="target"></span>
                                Nmap Scan
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="script_upload.php">
                                <span data-feather="upload"></span>
                                Script Upload
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="cronjob_manager.php">
                                <span data-feather="clock"></span>
                                Cronjob Manager
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main Content -->
            <main class="col-md-10 ms-sm-auto px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">Kali Linux Network Tools Dashboard</h1>
                </div>

                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Nmap Scan</h5>
                                <p class="card-text">Perform network scans with customizable parameters.</p>
                                <a href="nmap_scan.php" class="btn btn-primary">Start Scan</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Script Upload</h5>
                                <p class="card-text">Upload and manage custom Nmap NSE scripts.</p>
                                <a href="script_upload.php" class="btn btn-secondary">Manage Scripts</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Cronjob Manager</h5>
                                <p class="card-text">Schedule and manage automated network scans.</p>
                                <a href="cronjob_manager.php" class="btn btn-info">Manage Cronjobs</a>
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
