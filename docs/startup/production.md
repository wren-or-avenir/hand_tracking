# Windows 部署指南

## 前置条件

- Windows 10 或 Windows 11（64 位）
- 可用摄像头
- Git
- Miniconda 或 Anaconda

## 安装

打开 PowerShell，克隆项目并进入目录：

```powershell
git clone https://github.com/wren-or-avenir/hand_tracking.git
cd hand_tracking
```

创建 Python 3.11 环境并安装依赖：

```powershell
conda create --name hand_tracking python=3.11 pip -y
conda activate hand_tracking
python -m pip install -r .\envs\requirements.txt
```

确认 MediaPipe 模型存在：

```powershell
Test-Path .\models\hand_landmarker.task
```

如果返回 `False`，下载官方模型：

```powershell
New-Item -ItemType Directory -Force .\models
Invoke-WebRequest -Uri https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task -OutFile .\models\hand_landmarker.task
```

## 运行

启动实时摄像头效果：

```powershell
.\scripts\run.cmd
```

如果打开的不是目标摄像头，切换设备编号：

```powershell
.\scripts\run.cmd --camera 1
```

按 `q` 或 `Esc` 退出。

默认效果不透明度为 `0.65`；数值越低越透明：

```powershell
.\scripts\run.cmd --opacity 0.5
```

## 验证

不使用摄像头检查应用组装：

```powershell
.\scripts\run.cmd --mock
```

运行核心与渲染测试：

```powershell
conda run --name hand_tracking python .\tests\test_pipeline.py
```

看到 `pipeline checks passed` 即为通过。

## 常见问题

- 找不到 `conda`：改用 Anaconda Prompt，或先执行 `conda init powershell` 后重启 PowerShell。
- 无法打开摄像头：关闭正在占用摄像头的软件，再尝试 `--camera 1`、`--camera 2`。
- 提示模型缺失：重新执行上面的官方模型下载命令。
- MediaPipe 安装失败：确认 `python --version` 为 Python 3.11，并使用 64 位 Windows。
