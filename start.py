#!/usr/bin/env python3
"""
LightRAG API服务器启动脚本
支持本地开发和Railway云平台部署
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """配置日志系统"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def detect_railway_environment():
    """检测是否在Railway环境中运行"""
    railway_indicators = [
        'RAILWAY_ENVIRONMENT',
        'RAILWAY_PROJECT_ID',
        'RAILWAY_SERVICE_ID',
        'RAILWAY_DEPLOYMENT_ID'
    ]
    
    is_railway = any(os.getenv(indicator) for indicator in railway_indicators)
    
    if is_railway:
        print("🚂 检测到Railway部署环境")
        print(f"   - Railway项目ID: {os.getenv('RAILWAY_PROJECT_ID', 'N/A')}")
        print(f"   - Railway服务ID: {os.getenv('RAILWAY_SERVICE_ID', 'N/A')}")
        print(f"   - Railway部署ID: {os.getenv('RAILWAY_DEPLOYMENT_ID', 'N/A')}")
    else:
        print("💻 检测到本地开发环境")
    
    return is_railway

def load_environment():
    """加载环境变量"""
    from dotenv import load_dotenv
    
    is_railway = detect_railway_environment()
    
    if is_railway:
        # Railway环境：优先加载.env.railway配置
        railway_env = project_root / '.env.railway'
        if railway_env.exists():
            load_dotenv(railway_env)
            print(f"✓ 已加载Railway环境配置: {railway_env}")
        else:
            print(f"⚠ 未找到Railway环境配置文件: {railway_env}")
    
    # 加载主.env文件（作为备用配置）
    env_file = project_root / '.env'
    if env_file.exists():
        load_dotenv(env_file, override=False)  # 不覆盖已有的环境变量
        print(f"✓ 已加载主环境配置: {env_file}")
    else:
        print(f"⚠ 未找到主环境配置文件: {env_file}")
    
    # 显示关键配置信息
    print("\n📋 关键配置信息:")
    print(f"   - HOST: {os.getenv('HOST', '0.0.0.0')}")
    print(f"   - PORT: {os.getenv('PORT', '9621')}")
    print(f"   - LLM_BINDING: {os.getenv('LLM_BINDING', 'openai')}")
    print(f"   - LLM_MODEL: {os.getenv('LLM_MODEL', 'N/A')}")
    print(f"   - LLM_BINDING_HOST: {os.getenv('LLM_BINDING_HOST', 'N/A')}")
    print(f"   - EMBEDDING_BINDING: {os.getenv('EMBEDDING_BINDING', 'openai')}")
    print(f"   - EMBEDDING_MODEL: {os.getenv('EMBEDDING_MODEL', 'N/A')}")
    print(f"   - POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'N/A')}")
    print(f"   - POSTGRES_DATABASE: {os.getenv('POSTGRES_DATABASE', 'N/A')}")

def main():
    """主启动函数"""
    logger = setup_logging()
    logger.info("🚀 启动 LightRAG API 服务器...")
    
    # 加载环境变量
    load_environment()
    
    try:
        # 导入并启动服务器
        from lightrag.api.lightrag_server import main as server_main
        server_main()
    except ImportError as e:
        logger.error(f"❌ 导入错误: {e}")
        logger.error("请确保已正确安装 LightRAG 依赖")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()