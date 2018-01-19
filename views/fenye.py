#!/usr/bin/env python
#coding:utf-8


class fen_ye_lei:
    def __init__(self,dang_qian_ye,shu_ju,tiao_shu,ye_ma_shu,qian_hou_ye,url):
        """
        一个参数接收当前页
        第一个参数，接收分页数据列表
        第二个参数，接收每页显示多少条数据
        第三个参数，每页显示多少个页码
        第四个参数，显示当前页码前几个和后几个页码，需要结合每页显示多少个页码计算
        第五个参数，分页连接url后缀，也就是路由映射的后缀
        """
        try:                                            
            dang_qian_ye = int(dang_qian_ye)            
        except:                                         
            dang_qian_ye = 1                            
        if dang_qian_ye < 1:                            
            dang_qian_ye = 1                            

        self.dang_qian_ye = dang_qian_ye                
        self.shu_ju = shu_ju                            
        self.tiao_shu = tiao_shu                        
        self.ye_ma_shu = ye_ma_shu                      
        self.qian_hou_ye = qian_hou_ye                  
        self.url = url                                  


        
        zong_ye_ma, c = divmod(len(self.shu_ju), self.tiao_shu)   
        if c > 0:                                       
            zong_ye_ma += 1                             
        self.zong_ye_ma = zong_ye_ma                    


    def shu_ju_fan_wei(self):
        """
        shu_ju_fan_wei()方法，返回每页获取范围数据
        """
        
        qi_shi = (self.dang_qian_ye - 1) * self.tiao_shu     
        jie_shu = self.dang_qian_ye * self.tiao_shu          
        xian_shi = self.shu_ju[qi_shi:jie_shu]               
        return xian_shi


    def xian_shi_ye_ma(self):
        """
        xian_shi_ye_ma()方法，返回页码数据
        """
        
        
        
        if self.zong_ye_ma < self.ye_ma_shu:                            
            s = 1                                                       
            t = self.zong_ye_ma                                         
        else:
            if self.dang_qian_ye <= self.qian_hou_ye + 1:               
                s = 1                                                   
                t = self.ye_ma_shu                                      
            else:
                if (self.dang_qian_ye + self.qian_hou_ye) > self.zong_ye_ma:    
                    s = self.zong_ye_ma - (self.ye_ma_shu - 1)                  
                    t = self.zong_ye_ma                                         
                else:
                    s = self.dang_qian_ye - self.qian_hou_ye                    
                    t = self.dang_qian_ye + self.qian_hou_ye                    

        ye_ma_lie_biao = []                                                     

        
        sh_temp = '<li><a href="%s1">首页</a></li>' % (self.url)
        ye_ma_lie_biao.append(sh_temp)

        
        if self.dang_qian_ye <= 1:
            shye = '<li><a href="javascript:void(0);">上一页</a></li>'
            ye_ma_lie_biao.append(shye)
        else:
            shye = '<li><a href="%s%s">上一页</a></li>' %(self.url,self.dang_qian_ye-1)
            ye_ma_lie_biao.append(shye)

        for i in range(s, t + 1):                                               
            if i == self.dang_qian_ye:                                          
                temp = '<li class="yem"><a href="%s%s">%s</a></li>' % (self.url,i, i)   
            else:
                temp = '<li><a href="%s%s">%s</a></li>' % (self.url,i, i)               
            ye_ma_lie_biao.append(temp)                                             

        
        if self.dang_qian_ye >= self.zong_ye_ma:
            xye = '<li><a href="javascript:void(0);">下一页</a></li>'
            ye_ma_lie_biao.append(xye)
        else:
            xye = '<li><a href="%s%s">下一页</a></li>' %(self.url,self.dang_qian_ye+1)
            ye_ma_lie_biao.append(xye)

        
        wei_temp = '<li><a href="%s%s">尾页</a></li>' % (self.url,self.zong_ye_ma)
        ye_ma_lie_biao.append(wei_temp)

        xian_shi = "\n".join(ye_ma_lie_biao)                                        
        return xian_shi
