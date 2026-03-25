"""Flow2API - Main Entry Point"""

# ========== 中文路径 SSL 证书修复补丁 ==========
# 当项目路径包含中文时, curl_cffi 无法定位 cacert.pem
# 此补丁将证书复制到纯英文临时目录并设置环境变量
import os, shutil, tempfile
try:
    import certifi
    _original_cert = certifi.where()
    # 检测路径是否包含非 ASCII 字符
    try:
        _original_cert.encode('ascii')
    except UnicodeEncodeError:
        _safe_dir = os.path.join(tempfile.gettempdir(), 'flow2api_certs')
        os.makedirs(_safe_dir, exist_ok=True)
        _safe_cert = os.path.join(_safe_dir, 'cacert.pem')
        shutil.copy2(_original_cert, _safe_cert)
        os.environ['CURL_CA_BUNDLE'] = _safe_cert
        os.environ['REQUESTS_CA_BUNDLE'] = _safe_cert
        os.environ['SSL_CERT_FILE'] = _safe_cert
        print(f"[补丁] SSL 证书已复制到安全路径: {_safe_cert}")
except Exception as _e:
    print(f"[补丁] SSL 修复跳过: {_e}")
# ========== 补丁结束 ==========

from src.main import app
import uvicorn

if __name__ == "__main__":
    from src.core.config import config
    import threading
    import webbrowser
    import time
    
    def open_admin_panel():
        # 等待框架启动后自动唤起浏览器
        time.sleep(1.5)
        print("🌍 正在为您打开默认浏览器进入【创作实验室】...")
        webbrowser.open(f"http://127.0.0.1:{config.server_port}/manage")

    # 启动异步线程打开网页
    threading.Thread(target=open_admin_panel, daemon=True).start()

    uvicorn.run(
        "src.main:app",
        host=config.server_host,
        port=config.server_port,
        reload=False
    )
