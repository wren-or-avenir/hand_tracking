# Hand Tracking Corner Pin

复刻 `design/fork_video.mp4` 中的双手四指尖实时画面形变效果。

当前完成第一阶段：数据链路、接口、四点映射、状态机与离线 mock。运行：

```powershell
.\scripts\run.cmd --mock
python .\tests\test_pipeline.py
```

设计与后续步骤见 [docs/design/hand_effect.md](docs/design/hand_effect.md)。
