## docker指令
首先要先寫好dockerfile

#### 啟動部分
* "docker build -t test -f [Docker File Name] ." ->(build一個叫test的image)
* "docker run -itd test" ->(把test這個image啟動,變成container)
* "docker images" ->(看一下有哪些images)
* "docker ps -a" ->(看一下每個container的狀態:image,有沒有啟動)
* "docker start [container ID]" ->(重啟該container)
* "docker exec -it [container ID] bash" ->(在這個container做/bin/bash)

#### 進到python後
* "apt update" ->(update apt)
* "apt install vim" ->(update vim)
* "exit"->(結束python)
* "vim [01. tagging_transformer.py]"->(修改python file)
 * i(編輯)/ :q(quit)+Enter/ :wq(save)

#### 刪除部分
* "docker stop [container ID]" ->(停止該container)
* "docker rm [container ID1] [container ID2]" ->(刪除container)
* "docker rmi [image name1] [image name2]" ->(刪除image)

#### 0302:新的指令
* "docker run -itd -p 6666:6666 [image name]" ->(讓container 6666的port與外部6666相同)
* "docker tag [old image name]:[old tag] [new image name]:[new tag]" ->(改images的tag)
* "docker save [image name]>[file name.tar]" ->(把images存成改成tar)
* "docker load<[file name.tar]" ->(把tar存成images)
* "docker logs" ->(看一下logs)
