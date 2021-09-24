
# 以图搜图
## 说明

根据小图像查找在大图中的坐标位置,支持对PhotoShop图像文件(PSD,PSB)的检索

## 安装说明
将convertpoint目录拷贝至工作目录内


## 依赖
```bash
Pillow~=8.3.2
numpy~=1.21.2
psd-tools~=1.9.18
opencv-python~=4.5.3.56
matplotlib~=3.4.3
```

## 示例说明

```bash
# 引入convertpoint
import convertpoint
# 构造参数1：大图，参数2：小图 
# 声明方法
p = convertpoint.ImagePoint('italy.jpg', 'small.jpg')
# 以matplotlib预览
p.show()
```

|  对象函数   | 参数  | 返回  | 说明
|  ----  | ----  |----  | ----  |
| show()  |  |  | 以matplotlib预览 |
| setEnlargePixel(int)  | 像素 | | 小图向四周扩大范围 |
| enlarge()  |  | | 根据扩大的像素生成新的图片，文件命名为expand_小图的名称 |
| getPILImage()  |  | Image| 获得PIL对象  |
| getPoint()  |  | tuple| 获得坐标  |
## License
<img src="https://cdn.e-dunhuang.com/images/logo.png">

Power by:叶青  
QQ:215777  
Version:1.0   
