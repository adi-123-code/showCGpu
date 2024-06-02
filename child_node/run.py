import argparse

from app import app

if __name__ == "__main__":
    # 子节点可以运行在不同的端口上，将端口参数传递给 app.run() 方法
    parser = argparse.ArgumentParser(description="Run the app on a specific port")
    parser.add_argument('--port', type=int, default=5001, help="The port to run the app on")
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)

