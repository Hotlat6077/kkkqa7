import { pipeline } from '@huggingface/transformers';

// ==================== DOM Elements ====================
const uploadSection = document.getElementById('upload-section');
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const loadingSection = document.getElementById('loading-section');
const loadingText = document.getElementById('loading-text');
const loadingSub = document.getElementById('loading-sub');
const progressBar = document.getElementById('progress-bar');
const dualView = document.getElementById('dual-view');
const originalVideo = document.getElementById('original-video');
const detectionCanvas = document.getElementById('detection-canvas');
const statusLabel = document.getElementById('status-label');
const fpsElem = document.getElementById('fps-counter');
const playPauseBtn = document.getElementById('play-pause-btn');
const ppIcon = document.getElementById('pp-icon');
const stopBtn = document.getElementById('stop-btn');
const newVideoBtn = document.getElementById('new-video-btn');
const seekBar = document.getElementById('seek-bar');
const timeDisplay = document.getElementById('time-display');
const thresholdSlider = document.getElementById('threshold');
const threshVal = document.getElementById('thresh-val');
const detectCountElem = document.getElementById('detect-count');

const detCtx = detectionCanvas.getContext('2d');

// ==================== State ====================
let detector = null;
let threshold = 0.5;
let isPlaying = false;
let animFrameId = null;
let lastTime = 0;
let totalDetections = 0;
let processedFrames = 0;
let pendingFile = null;

const COLORS = ['#C9A962', '#B08D57', '#C77D58', '#8A8A8A', '#A88B4A', '#D4B876', '#6B5B4F', '#7A6F5D',
    '#00F0FF', '#0080FF', '#4ADE80', '#FBBF24', '#F87171', '#A78BFA', '#FB923C', '#38BDF8'];
const labelColorMap = new Map();
let nextColorIndex = 0;

function getColorForLabel(label) {
    if (!labelColorMap.has(label)) {
        labelColorMap.set(label, COLORS[nextColorIndex % COLORS.length]);
        nextColorIndex++;
    }
    return labelColorMap.get(label);
}

// ==================== Upload Handling ====================
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('video/')) {
        handleVideoFile(file);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleVideoFile(file);
    fileInput.value = '';
});

async function handleVideoFile(file) {
    pendingFile = file;

    if (!detector) {
        uploadSection.style.display = 'none';
        loadingSection.style.display = 'flex';
        await loadModel();
    }

    startVideoPlayback(file);
}

// ==================== Model Loading ====================
async function loadModel() {
    loadingText.textContent = '加载模型中...';
    loadingSub.textContent = '下载 RF-DETR Medium (fp32)';
    progressBar.style.width = '0%';

    try {
        detector = await pipeline('object-detection', 'onnx-community/rfdetr_medium-ONNX', {
            device: 'webgpu',
            dtype: 'fp32',
            progress_callback: (progress) => {
                if (progress.status === 'downloading') {
                    const percent = progress.progress ? progress.progress.toFixed(1) : 0;
                    loadingSub.textContent = `下载中... ${percent}%`;
                    progressBar.style.width = percent + '%';
                } else if (progress.status === 'loading') {
                    loadingText.textContent = '编译着色器...';
                    loadingSub.textContent = '预热中，请稍候';
                    progressBar.style.width = '100%';
                }
            }
        });

        statusLabel.textContent = '模型就绪';
        document.querySelector('.status-online').classList.add('active');
    } catch (e) {
        loadingText.textContent = '模型加载失败';
        loadingSub.textContent = e.message;
        console.error('Model load error:', e);
        throw e;
    }
}

// ==================== Video Playback ====================
function startVideoPlayback(file) {
    loadingSection.style.display = 'none';
    uploadSection.style.display = 'none';
    dualView.style.display = 'flex';

    const url = URL.createObjectURL(file);
    originalVideo.src = url;

    originalVideo.addEventListener('loadedmetadata', () => {
        detectionCanvas.width = originalVideo.videoWidth;
        detectionCanvas.height = originalVideo.videoHeight;
        updateTimeDisplay();
        play();
    }, { once: true });

    originalVideo.load();
}

function play() {
    if (isPlaying) return;
    isPlaying = true;
    originalVideo.play();
    ppIcon.textContent = 'pause';
    statusLabel.textContent = '检测中...';
    lastTime = performance.now();
    animFrameId = requestAnimationFrame(loop);
}

function pause() {
    isPlaying = false;
    originalVideo.pause();
    ppIcon.textContent = 'play_arrow';
    statusLabel.textContent = '已暂停';
    if (animFrameId) {
        cancelAnimationFrame(animFrameId);
        animFrameId = null;
    }
}

function stop() {
    pause();
    originalVideo.currentTime = 0;
    seekBar.value = 0;
    updateTimeDisplay();
    statusLabel.textContent = '已停止';

    detCtx.clearRect(0, 0, detectionCanvas.width, detectionCanvas.height);
    document.getElementById('detections-container').innerHTML = '';
    detectCountElem.textContent = '0 个目标';
}

// ==================== Controls ====================
playPauseBtn.addEventListener('click', () => {
    if (isPlaying) pause();
    else play();
});

stopBtn.addEventListener('click', stop);

newVideoBtn.addEventListener('click', () => {
    stop();
    if (originalVideo.src) URL.revokeObjectURL(originalVideo.src);
    originalVideo.removeAttribute('src');

    dualView.style.display = 'none';
    uploadSection.style.display = 'flex';
    statusLabel.textContent = '等待上传';

    totalDetections = 0;
    processedFrames = 0;
    document.getElementById('total-count').textContent = '0';
    document.getElementById('frame-count').textContent = '0';
    document.getElementById('avg-conf').textContent = '0%';
    document.getElementById('processed-frames').textContent = '0';
});

thresholdSlider.addEventListener('input', (e) => {
    threshold = parseFloat(e.target.value);
    threshVal.textContent = threshold.toFixed(2);
});

seekBar.addEventListener('input', () => {
    const t = (seekBar.value / 100) * originalVideo.duration;
    originalVideo.currentTime = t;
    updateTimeDisplay();
});

originalVideo.addEventListener('ended', () => {
    pause();
    statusLabel.textContent = '播放完毕';
});

// ==================== Time Display ====================
function formatTime(s) {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
}

function updateTimeDisplay() {
    const cur = originalVideo.currentTime || 0;
    const dur = originalVideo.duration || 0;
    timeDisplay.textContent = `${formatTime(cur)} / ${formatTime(dur)}`;
    if (dur > 0) {
        seekBar.value = (cur / dur) * 100;
    }
}

// ==================== Detection Loop ====================
const inputCanvas = document.createElement('canvas');
const inputCtx = inputCanvas.getContext('2d');

async function loop() {
    if (!isPlaying) return;

    const now = performance.now();
    const dt = now - lastTime;
    lastTime = now;
    if (dt > 0) fpsElem.textContent = (1000 / dt).toFixed(1);

    updateTimeDisplay();

    const vw = originalVideo.videoWidth;
    const vh = originalVideo.videoHeight;
    if (vw === 0 || vh === 0) {
        animFrameId = requestAnimationFrame(loop);
        return;
    }

    inputCanvas.width = vw;
    inputCanvas.height = vh;
    inputCtx.drawImage(originalVideo, 0, 0, vw, vh);

    let results = [];
    try {
        results = await detector(inputCanvas, { threshold, percentage: true });
    } catch (e) {
        console.error('Detection error:', e);
    }

    drawDetectionFrame(vw, vh, results);
    updateStats(results);

    animFrameId = requestAnimationFrame(loop);
}

// ==================== Drawing ====================
function drawDetectionFrame(w, h, results) {
    detectionCanvas.width = w;
    detectionCanvas.height = h;

    detCtx.drawImage(originalVideo, 0, 0, w, h);

    detCtx.font = '600 14px system-ui';
    detCtx.lineWidth = 2.5;

    for (const { box, label, score } of results) {
        const color = getColorForLabel(label);
        const x1 = box.xmin * w;
        const y1 = box.ymin * h;
        const bw = (box.xmax - box.xmin) * w;
        const bh = (box.ymax - box.ymin) * h;

        detCtx.strokeStyle = color;
        detCtx.shadowColor = color;
        detCtx.shadowBlur = 8;
        detCtx.beginPath();
        detCtx.roundRect(x1, y1, bw, bh, 4);
        detCtx.stroke();
        detCtx.shadowBlur = 0;

        const text = `${label} ${(score * 100).toFixed(0)}%`;
        const tw = detCtx.measureText(text).width;
        const tagH = 22;
        const tagY = y1 - tagH - 2;

        detCtx.fillStyle = color;
        detCtx.beginPath();
        detCtx.roundRect(x1, tagY < 0 ? y1 : tagY, tw + 12, tagH, 4);
        detCtx.fill();

        detCtx.fillStyle = '#fff';
        detCtx.fillText(text, x1 + 6, (tagY < 0 ? y1 : tagY) + 16);
    }
}

// ==================== Stats ====================
let confSum = 0;
let confCount = 0;

function updateStats(results) {
    processedFrames++;
    totalDetections += results.length;

    results.forEach(r => {
        confSum += r.score;
        confCount++;
    });

    document.getElementById('total-count').textContent = totalDetections;
    document.getElementById('frame-count').textContent = results.length;
    document.getElementById('processed-frames').textContent = processedFrames;

    detectCountElem.textContent = `${results.length} 个目标`;

    if (confCount > 0) {
        document.getElementById('avg-conf').textContent = ((confSum / confCount) * 100).toFixed(0) + '%';
    }

    const container = document.getElementById('detections-container');
    container.innerHTML = '';
    results.forEach(r => {
        const color = getColorForLabel(r.label);
        const tag = document.createElement('div');
        tag.className = 'detection-tag';
        tag.style.borderColor = color;
        tag.innerHTML = `<span class="tag-label">${r.label}</span><span class="tag-score">${(r.score * 100).toFixed(0)}%</span>`;
        container.appendChild(tag);
    });
}
