# Hand Tracking Corner Pin

一个由双手控制的实时摄像头特效：程序连接两只手对应的拇指、食指、中指和小拇指，形成三个四边形区域，并分别叠加反色、霓虹和漫画滤镜。

效果参考：[design/fork_video.mp4](design/fork_video.mp4)。

## 环境要求

- Windows 10/11（64 位）
- Miniconda 或 Anaconda
- Python 3.11
- 可用摄像头

## 安装

```powershell
conda create --name hand_tracking python=3.11 pip -y
conda activate hand_tracking
python -m pip install -r .\envs\requirements.txt
```

仓库应包含 MediaPipe 模型 `models/hand_landmarker.task`。完整部署和模型补装步骤见 [Windows 部署指南](docs/startup/production.md)。

## 运行

```powershell
.\scripts\run.cmd
```

将两只手同时放入画面，展开拇指、食指、中指和小拇指即可显示三个局部滤镜区域。按 `q` 或 `Esc` 退出。

常用参数：

```powershell
.\scripts\run.cmd --camera 1        # 切换摄像头
.\scripts\run.cmd --opacity 0.5     # 调整滤镜不透明度（0～1）
.\scripts\run.cmd --confidence 0.7  # 调整手部检测阈值
.\scripts\run.cmd --min-area 0.003  # 忽略更小的四边形区域
```

## 离线验证

不连接摄像头检查应用流程：

```powershell
.\scripts\run.cmd --mock
```

运行核心逻辑与渲染测试：

```powershell
conda run --name hand_tracking python .\tests\test_pipeline.py
```

看到 `pipeline checks passed` 即表示通过。

## 项目结构

```text
app/main.py                 应用入口与参数解析
src/hand_effect/            手部追踪、区域计算和滤镜渲染
models/hand_landmarker.task MediaPipe 手部模型
scripts/run.cmd             Windows 启动脚本
tests/test_pipeline.py      离线自检
docs/                       设计与部署文档
```

实现细节和数据流见 [效果设计](docs/design/hand_effect.md)。
