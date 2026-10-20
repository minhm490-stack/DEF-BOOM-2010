import os
import winreg
import subprocess
import psutil
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Nội dung giao diện HTML/CSS/JS (Giao diện 20/10)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌸 Chúc Mừng Ngày 20/10 - Quản Lý Hệ Thống 🌸</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            font-family: 'Nunito', sans-serif;
            background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 100%);
            min-height: 100vh;
            color: #4a4a4a;
            position: relative;
            overflow-x: hidden;
        }

        .banner-2010 {
            background: linear-gradient(45deg, #ff6b81, #ff4757);
            color: white;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(255, 71, 87, 0.3);
            margin-bottom: 25px;
            text-align: center;
        }

        .banner-2010 h1 {
            font-family: 'Dancing Script', cursive;
            font-size: 2.8rem;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(255, 182, 193, 0.4);
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
        }

        .card-header {
            background-color: #ffb6c1;
            color: #d63031;
            font-weight: 700;
            border-radius: 15px 15px 0 0 !important;
            border-bottom: none;
        }

        .nav-tabs .nav-link {
            color: #d63031;
            font-weight: 600;
            border: none;
            border-radius: 10px 10px 0 0;
            margin-right: 5px;
        }

        .nav-tabs .nav-link.active {
            background-color: #ff6b81;
            color: white !important;
        }

        .table-wrapper {
            max-height: 420px;
            overflow-y: auto;
        }

        .table-pink th {
            background-color: #ffccd5;
            color: #c0392b;
            position: sticky;
            top: 0;
            z-index: 1;
        }

        .btn-custom-pink {
            background-color: #ff4757;
            color: white;
            border-radius: 20px;
            padding: 8px 20px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }

        .btn-custom-pink:hover {
            background-color: #ff6b81;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 10px rgba(255, 71, 87, 0.4);
        }

        .btn-custom-outline {
            border: 2px solid #ff4757;
            color: #ff4757;
            border-radius: 20px;
            font-weight: 600;
            background: transparent;
        }

        .btn-custom-outline:hover {
            background-color: #ff4757;
            color: white;
        }

        .flower {
            position: fixed;
            top: -10%;
            font-size: 20px;
            user-select: none;
            z-index: 1000;
            pointer-events: none;
            animation: fall linear infinite;
        }

        @keyframes fall {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; }
            100% { transform: translateY(105vh) rotate(360deg); opacity: 0; }
        }
    </style>
</head>
<body>

    <script>
        const flowers = ['🌸', '🌺', '🌹', '🌷', '✨'];
        for (let i = 0; i < 25; i++) {
            let flower = document.createElement('div');
            flower.className = 'flower';
            flower.innerHTML = flowers[Math.floor(Math.random() * flowers.length)];
            flower.style.left = Math.random() * 100 + 'vw';
            flower.style.animationDuration = (Math.random() * 3 + 4) + 's';
            flower.style.animationDelay = Math.random() * 5 + 's';
            flower.style.fontSize = (Math.random() * 10 + 15) + 'px';
            document.body.appendChild(flower);
        }
    </script>

    <div class="container py-4">
        <div class="banner-2010">
            <h1>💐 Chúc Mừng Ngày Phụ Nữ Việt Nam 20/10 💐</h1>
            <p class="mb-0 fs-5">Chúc bạn luôn xinh đẹp, rạng rỡ, hạnh phúc và hệ thống máy tính luôn chạy siêu mượt mà!</p>
        </div>

        <div class="row g-4">
            <div class="col-lg-8">
                <div class="card p-3">
                    <ul class="nav nav-tabs" id="myTab" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="installed-tab" data-bs-toggle="tab" data-bs-target="#installed" type="button" role="tab">
                                📦 Ứng Dụng Đã Cài
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="running-tab" data-bs-toggle="tab" data-bs-target="#running" type="button" role="tab">
                                ⚡ Tiến Trình Đang Chạy
                            </button>
                        </li>
                    </ul>

                    <div class="tab-content pt-3" id="myTabContent">
                        <div class="tab-pane fade show active" id="installed" role="tabpanel">
                            <div class="table-wrapper">
                                <table class="table table-hover align-middle">
                                    <thead class="table-pink">
                                        <tr>
                                            <th>Tên Phần Mềm / Ứng Dụng</th>
                                            <th>Phiên Bản</th>
                                            <th>Nhà Phát Hành</th>
                                        </tr>
                                    </thead>
                                    <tbody id="installed-body">
                                        <tr><td colspan="3" class="text-center text-muted">Đang tải danh sách...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="tab-pane fade" id="running" role="tabpanel">
                            <div class="table-wrapper">
                                <table class="table table-hover align-middle">
                                    <thead class="table-pink">
                                        <tr>
                                            <th>PID</th>
                                            <th>Tên Tiến Trình</th>
                                            <th>CPU (%)</th>
                                            <th>RAM (MB)</th>
                                        </tr>
                                    </thead>
                                    <tbody id="running-body">
                                        <tr><td colspan="4" class="text-center text-muted">Đang tải danh sách...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div class="mt-3 pt-3 border-top d-flex flex-wrap gap-2">
                        <button class="btn btn-custom-outline" onclick="loadData()">
                            <i class="fa-solid fa-rotate-right"></i> Làm Mới
                        </button>
                        <button class="btn btn-custom-pink" onclick="uninstallSelectedApp()">
                            <i class="fa-solid fa-trash-can"></i> Gỡ Cài Đặt App Đã Chọn
                        </button>
                        <button class="btn btn-custom-pink bg-danger" onclick="killSelectedProcess()">
                            <i class="fa-solid fa-circle-stop"></i> Tắt App Đang Chạy
                        </button>
                    </div>
                </div>
            </div>

            <div class="col-lg-4">
                <div class="card h-100">
                    <div class="card-header text-center">
                        💖 Biểu Đồ Tài Nguyên Máy Tính 💖
                    </div>
                    <div class="card-body d-flex flex-column justify-content-around">
                        <div>
                            <h6 class="text-center font-weight-bold text-danger mb-2">🔥 Sử Dụng CPU</h6>
                            <div style="height: 180px;">
                                <canvas id="cpuChart"></canvas>
                            </div>
                        </div>
                        <hr class="my-2">
                        <div>
                            <h6 class="text-center font-weight-bold text-primary mb-2">🌸 Sử Dụng RAM</h6>
                            <div style="height: 180px;">
                                <canvas id="ramChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        let selectedApp = null;
        let selectedProcess = null;

        const cpuCtx = document.getElementById('cpuChart').getContext('2d');
        const ramCtx = document.getElementById('ramChart').getContext('2d');

        const cpuChart = new Chart(cpuCtx, {
            type: 'doughnut',
            data: {
                labels: ['Đang Dùng (%)', 'Rảnh (%)'],
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ['#ff4757', '#7bed9f']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        const ramChart = new Chart(ramCtx, {
            type: 'doughnut',
            data: {
                labels: ['Đang Dùng (%)', 'Rảnh (%)'],
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ['#ff6b81', '#70a1ff']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        async function loadData() {
            try {
                const res = await fetch('/api/data');
                const data = await res.json();

                const installedBody = document.getElementById('installed-body');
                installedBody.innerHTML = '';
                data.installed_apps.forEach(app => {
                    const tr = document.createElement('tr');
                    tr.style.cursor = 'pointer';
                    tr.innerHTML = `<td><b>${app.name}</b></td><td>${app.version}</td><td>${app.publisher}</td>`;
                    tr.onclick = () => {
                        document.querySelectorAll('#installed-body tr').forEach(r => r.classList.remove('table-active'));
                        tr.classList.add('table-active');
                        selectedApp = app.name;
                    };
                    installedBody.appendChild(tr);
                });

                const runningBody = document.getElementById('running-body');
                runningBody.innerHTML = '';
                data.running_apps.forEach(proc => {
                    const tr = document.createElement('tr');
                    tr.style.cursor = 'pointer';
                    tr.innerHTML = `<td>${proc.pid}</td><td><b>${proc.name}</b></td><td>${proc.cpu}%</td><td>${proc.ram} MB</td>`;
                    tr.onclick = () => {
                        document.querySelectorAll('#running-body tr').forEach(r => r.classList.remove('table-active'));
                        tr.classList.add('table-active');
                        selectedProcess = proc;
                    };
                    runningBody.appendChild(tr);
                });

                cpuChart.data.datasets[0].data = [data.cpu_usage, (100 - data.cpu_usage).toFixed(1)];
                cpuChart.update();

                ramChart.data.datasets[0].data = [data.ram_usage, (100 - data.ram_usage).toFixed(1)];
                ramChart.update();

            } catch (err) {
                console.error("Lỗi khi kết nối server:", err);
            }
        }

        async function uninstallSelectedApp() {
            if (!selectedApp) {
                alert("🌸 Vui lòng chọn 1 ứng dụng trong danh sách 'Ứng Dụng Đã Cài'!");
                return;
            }
            if (confirm(`Bạn có chắc chắn muốn GỠ CÀI ĐẶT ứng dụng:\n\n'${selectedApp}'?`)) {
                const res = await fetch('/api/uninstall', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({app_name: selectedApp})
                });
                const result = await res.json();
                alert(result.message);
                selectedApp = null;
                loadData();
            }
        }

        async function killSelectedProcess() {
            if (!selectedProcess) {
                alert("🌸 Vui lòng chuyển qua tab 'Tiến Trình Đang Chạy' và chọn 1 ứng dụng!");
                return;
            }
            if (confirm(`Bạn có chắc muốn tắt ứng dụng '${selectedProcess.name}' (PID: ${selectedProcess.pid})?`)) {
                const res = await fetch('/api/kill', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({pid: selectedProcess.pid})
                });
                const result = await res.json();
                alert(result.message);
                selectedProcess = null;
                loadData();
            }
        }

        loadData();
        setInterval(loadData, 5000);
    </script>
</body>
</html>
"""

def get_all_installed_apps():
    apps = []
    uninstall_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for key_path in uninstall_keys:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    sub_key_name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, sub_key_name)
                    app_name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                    try:
                        version, _ = winreg.QueryValueEx(sub_key, "DisplayVersion")
                    except FileNotFoundError:
                        version = "N/A"
                    try:
                        publisher, _ = winreg.QueryValueEx(sub_key, "Publisher")
                    except FileNotFoundError:
                        publisher = "Không rõ"
                    if app_name and app_name.strip():
                        apps.append({"name": app_name.strip(), "version": str(version), "publisher": str(publisher)})
                except Exception:
                    pass
        except Exception:
            pass
    unique_apps = {app['name']: app for app in apps}.values()
    return sorted(list(unique_apps), key=lambda x: x['name'].lower())