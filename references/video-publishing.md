# 视频作品发布

在个人网站中新增 MP4、视频封面或视频画廊时阅读本文件。目标是让媒体由正式域名稳定播放，并用可重复的检查替代上传后的反复试错。

## 先确认限制，再处理视频

1. 找到真实托管平台、静态发布目录、生产分支和单文件上限。控制台、部署配置和当前平台文档的限制优先，不要把某次经验值当成所有平台的固定规则。
2. 阿里云 ESA Pages 曾出现单文件 25 MB 限制；使用时仍应重新确认。设置 `--max-bytes 25000000` 并留出余量，避免把“25 MB”误解成 25 MiB。
3. 记录原视频时长、分辨率、视频编码、音频编码和大小。网页交付优先使用 H.264、AAC、`yuv420p` 和 MP4。
4. 在修改首页前完成转码和完整解码检查。否则页面已经做好却因文件超限或编码不兼容而返工。

可使用 `ffprobe` 获取媒体信息：

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,codec_type,width,height,pix_fmt -of json input.mp4
```

## 转码与封面

下面是兼容性优先的起点。根据实际文件大小调整 `-crf`、分辨率和音频码率；数值越大，文件通常越小。

```bash
ffmpeg -i input.mp4 -vf "scale='min(1920,iw)':-2" \
  -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart -map_metadata -1 output.mp4
```

- 短视频可保留 1080p；文件仍超限时先降到 720p，再逐步提高 CRF，避免一次过度压缩。
- `+faststart` 把 MP4 元数据移到文件前部，便于网页尽快读取时长并开始分段加载。
- `-map_metadata -1` 去掉不需要的来源设备和编辑软件元数据。
- 转码完成后执行完整解码检查：

```bash
ffmpeg -v error -i output.mp4 -f null -
```

从能代表内容的时间点生成封面，不要使用纯黑首帧：

```bash
ffmpeg -ss 00:00:03 -i output.mp4 -frames:v 1 -q:v 2 poster.jpg
```

## 页面接入

把视频和封面放在作品集自己的静态目录中，使用同源相对路径。不要把本机绝对目录、用户名或临时外链写进 HTML。

```html
<video controls preload="metadata" playsinline poster="assets/media/poster.jpg">
  <source src="assets/media/video.mp4" type="video/mp4">
</video>
```

- `controls` 提供真实播放控制；`playsinline` 避免移动端强制全屏；`preload="metadata"` 在流量和可用性之间取得平衡。
- 每个视频都应有独立标题、说明和准确封面；不得用占位按钮冒充可播放内容。
- 响应式布局应检查视频自然宽高比、卡片宽度、移动端单栏和横向溢出。
- 在静态目录运行：

```bash
python scripts/check-video-release.py path/to/public --max-bytes 25000000
```

该脚本检查同源路径、文件存在、MP4 签名、封面、控件、`playsinline`、`preload` 和单文件上限。平台限制不是 25,000,000 字节时必须显式修改参数。

## CSP 与生产分支

同源视频至少需要：

```text
media-src 'self';
```

如果保留可信旧媒体域名，可写成 `media-src 'self' https://media.example.com;`。读取正式域名的真实 `Content-Security-Policy` 响应头，不要只看控制台表单。

部署前确认“生产分支”和“测试分支”的关系。部分平台允许测试分支构建，却不允许把该版本直接提升到生产环境。遇到生产版本选择框看不到测试版本时：

1. 不要反复点击发布或重复创建构建。
2. 确认生产环境允许的分支，通常是 `main`。
3. 把已经通过测试的提交合并或快进到生产分支。
4. 等待平台从生产分支生成新版本，再确认生产发布比例和提交 ID。

## 线上验收

按以下顺序检查，失败时能快速定位到文件、CDN、CSP 或浏览器层：

1. 首页 HTML 包含真实标题、视频和封面相对路径。
2. 视频 `HEAD` 返回 `200`、`Content-Type: video/mp4`、正确的 `Content-Length` 和 `Accept-Ranges: bytes`。
3. `Range: bytes=0-1023` 返回 `206`，并包含正确的 `Content-Range`。
4. 封面返回 `200` 和正确图片 MIME 类型。
5. CSP 的 `media-src` 允许视频来源。
6. 生产浏览器中检查 `videoWidth`、`videoHeight`、`duration`、`readyState` 和 `error`；元数据可用且 `error` 为空。
7. 检查桌面双栏或预期布局、窄屏单栏、控制台错误和实际播放控制。

示例命令：

```bash
curl -I https://www.example.com/assets/media/video.mp4
curl -sS -D - -o /dev/null -H "Range: bytes=0-1023" https://www.example.com/assets/media/video.mp4
```

浏览器仍显示旧占位内容时，先用带版本查询参数的 URL 对比，再检查浏览器缓存、边缘缓存和 ETag。只有确认线上 HTML 仍旧时才重新部署或清理缓存。

## 常见失败与处理

| 现象 | 优先检查 |
|---|---|
| 上传或构建拒绝大文件 | 平台单文件上限；重新压缩并留余量 |
| 视频地址 200，但页面无法播放 | CSP `media-src`、MIME、编码和浏览器 `video.error` |
| 页面能打开但拖动进度条失败 | `Accept-Ranges`、206 和 `Content-Range` |
| 测试版本可用，生产版本列表没有它 | 生产分支限制；合并已验证提交后重新构建 |
| 发布后仍看到旧占位卡片 | 浏览器缓存、CDN 节点缓存和正式域名实际 HTML |
| 控制台看似保存成功但响应头没变 | 使用 Enter 或明确提交操作后，重新读取公网响应头 |
