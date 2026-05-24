#!/usr/bin/env python3
"""
一键部署到腾讯云 COS 静态网站
用法: python3 deploy-cos.py
需要先设置环境变量或直接填入下方配置
"""

import os
from qcloud_cos import CosConfig, CosS3Client
import sys

# ========== 在这里填写你的配置 ==========
SECRET_ID  = os.environ.get("TENCENT_SECRET_ID",  "你的SecretId")
SECRET_KEY = os.environ.get("TENCENT_SECRET_KEY", "你的SecretKey")
REGION     = os.environ.get("COS_REGION",         "ap-guangzhou")
BUCKET     = os.environ.get("COS_BUCKET",         "你的Bucket名称-APPID")
# =======================================

LOCAL_FILE = "硅基时代核心资产-分析报告.html"
REMOTE_KEY = "index.html"

def check_config():
    if "你的SecretId" in SECRET_ID:
        print("❌ 请先填写上面的 SECRET_ID、SECRET_KEY、BUCKET")
        print("   获取方式: 腾讯云控制台 → 访问管理 → API密钥管理")
        return False
    return True

def deploy():
    config = CosConfig(Region=REGION, SecretId=SECRET_ID, SecretKey=SECRET_KEY)
    client = CosS3Client(config)
    
    # 上传文件
    with open(LOCAL_FILE, 'rb') as f:
        client.put_object(
            Bucket=BUCKET,
            Key=REMOTE_KEY,
            Body=f,
            ContentType='text/html; charset=utf-8',
            CacheControl='no-cache'
        )
    
    # 生成访问 URL
    url = f"https://{BUCKET}.cos.{REGION}.myqcloud.com/{REMOTE_KEY}"
    
    print("✅ 部署成功！")
    print(f"🔗 访问地址: {url}")
    print()
    print("💡 提示: 如需自定义域名或开启 CDN 加速，请在 COS 控制台配置")
    print("   如需开启静态网站托管，设置 Bucket 为「静态网站」模式即可")
    return url

if __name__ == "__main__":
    if check_config():
        deploy()
