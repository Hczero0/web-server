import os.path
import socket
import threading

def handle_client_request(new_socket):
        recv_data = new_socket.recv(4096)

        if len(recv_data) == 0:
            new_socket.close()
            return

        # 对二进制进行解码
        recv_content = recv_data.decode("utf-8")
        print(recv_content)
        request_list = recv_content.split(" ", maxsplit=2)
        request_path = request_list[1]
        print(request_path)

        if request_path == "/":
            request_path = "/index.html"
        #   判断访问的数据在不在文件内
        #1.if os.path.exists("static/" + request_path):
        # 2.try except
        try:
            # 打开文件中传送的网页数据
            # window上需要加上encoding="utf-8" 以为OPEN在windows上内置编码是gbk
            # 为了兼容图片打开 需要用rb
            with open("static" + request_path, "rb") as file:
                file_data = file.read()
        #   没找到网页 返回404指令
        except Exception as e:
            response_line = "HTTP/1.1 404 NOT FOUNd\r\n"
            # 相应头
            response_header = "server: pws/1.0\r\n"
            with open("static/error.html" , "rb") as file:
                file_data = file.read()
            response_body = file_data
            response = (response_line + response_header + "\r\n").encode("utf-8") + response_body
            new_socket.send(response)
        else:
            # 相应行
            response_line = "HTTP/1.1 200 OK\r\n"
            # 相应头
            response_header = "server: pws/1.0\r\n"
            # 响应体
            response_body = file_data

            response = (response_line + response_header + "\r\n").encode("utf-8") + response_body
            new_socket.send(response)
        finally:
            new_socket.close()

def main():
    # 创建TCP服务端的套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # =设置端口号复用
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口
    tcp_server_socket.bind(("", 9000))
    # 设置监听
    tcp_server_socket.listen(128)
    # 等待接受客户的连接请求
    while True:
        new_socket, ip_port = tcp_server_socket.accept()
        sub_thread = threading.Thread(target=handle_client_request, args=(new_socket,))
        sub_thread.setDaemon(True)
        sub_thread.start()


if __name__ == '__main__':
    main()