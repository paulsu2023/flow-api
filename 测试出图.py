import urllib.request
import urllib.error
import json
import base64
import os

# 配置区
API_URL = "http://localhost:8000/models/gemini-3.1-flash-image:generateContent"
API_KEY = "han1234" # 请确保这和您在 localhost:8000 后台里设置的 API Key 是一致的

# 要测试的提示词
prompt = "一只戴着墨镜的酷炫哈士奇，极简的摄影棚背景，8k超高清照片"

payload = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {"text": prompt}
            ]
        }
    ],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": "1:1",
            "imageSize": "1K"
        }
    }
}

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json"
}

req = urllib.request.Request(API_URL, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

print(f"==================================================")
print(f"🚀 开始测试反薅请求！")
print(f"📡 目标节点: {API_URL}")
print(f"🔑 使用 Key: {API_KEY}")
print(f"📝 绘图指令: {prompt}")
print(f"==================================================")
print(f"正在发送请求给本地基站，请耐心等待谷歌出图 (可能需要十几秒)...\n")

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        # 解析返回的数据
        try:
            # 尝试提取 base64 图片数据
            b64_data = result['candidates'][0]['content']['parts'][0]['inlineData']['data']
            image_bytes = base64.b64decode(b64_data)
            
            output_file = "test_output.jpg"
            with open(output_file, "wb") as f:
                f.write(image_bytes)
            
            print(f"✅ 测试成功！！！")
            print(f"🎉 成功从顶级内部节点获取到图片！已保存为当前目录下的: {output_file}")
            print(f"请打开 {output_file} 查看效果。")
            
        except KeyError:
            print("⚠️ 请求虽然成功了，但返回的内容格式不对，可能出图失败了。")
            print("完整返回内容如下：")
            print(json.dumps(result, indent=2, ensure_ascii=False))

except urllib.error.HTTPError as e:
    print(f"❌ HTTP 错误: {e.code} - {e.reason}")
    print(e.read().decode('utf-8'))
except urllib.error.URLError as e:
    print(f"❌ 连接失败: 无法连接到本地 {API_URL}")
    print("请确认您的《flow api反薅》发电机 (启动反薅服务.bat) 是否已经在后台成功启动，并且后台配置好了正确的 ST/AT 令牌！")
except Exception as e:
    print(f"❌ 发生未知错误: {e}")

input("\n按回车键退出...")
