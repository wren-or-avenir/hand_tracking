# Hand Tracking Corner Pin

复刻 `design/fork_video.mp4` 中由双手四指控制的多区域实时滤镜效果。

运行全屏摄像头效果（按 `q` 或 `Esc` 退出）：

```powershell
.\scripts\run.cmd
```

离线检查：

```powershell
.\scripts\run.cmd --mock
conda run --name hand_tracking python .\tests\test_pipeline.py
```

部署步骤见 [docs/startup/production.md](docs/startup/production.md)。

设计与后续步骤见 [docs/design/hand_effect.md](docs/design/hand_effect.md)。
