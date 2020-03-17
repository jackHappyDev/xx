#oc转js语法和调用辅助官方工具
		https://jspatch.com/Tools/convertor

##基础用法
		https://github.com/bang590/JSPatch/wiki/JSPatch-%E5%9F%BA%E7%A1%80%E7%94%A8%E6%B3%95#1-require

###参考
		https://www.jianshu.com/p/def489f40d68

		
#require,defineClass
###require 是引用的意思

	require('UIScreen')
	require('UIView')
	require('UIColor')
	require('UIbutton')  等
	

###defineClass 是重写的意思


如果线上有方法要修复那么就重写这个方法,直接调用jspatch来修复

假设是在PTHomeViewController 有个testFunction 数组越界闪退 那么我们修复的代码是这样的
		
		require("NSArray,UIView, UIColor'");
		defineClass("PTHomeViewController", {
    		testFunction: function() {
        	self.setArr([ "熊猫", "🐼", "熊猫棋牌" ]);
        	var str = self.arr().objectAtIndex(2);
        	console.log("个人中心页面JSPatch调用" , str);
    	}
	}, {});
为了更好的DEBUG 代码是否下发成功，这个时候我建议在代码中加入js的log来判断是否加载完毕，如果自己写的js语法有错误 jspatch 会从上到下执行 并且不执行错误的代码

		 console.log("XX功能JSPatch调用" );


#修复UI
###屏幕宽高的获取

		var width = require('UIScreen').mainScreen().bounds().width;
   		var heigth = require('UIScreen').mainScreen().bounds().height;

###Button 创建
		
		var btn = require('UIButton').alloc().initWithFrame({x:300, y:100, width:300, height:150});
   		self.view().addSubview(btn);
 
###View 创建
          
          var v = require('UIView').alloc().initWithFrame({x:500, y:100, width:300, height:150});
          v.setBackgroundColor(require('UIColor').redColor());
          self.view().addSubview(v);
          
###UIImageView 的创建并使用sdwebimage
		var v = require('UIImageView').alloc().initWithFrame({x:500, y:100, width:300, height:150});
		self.view().addSubview(v);
		v.sd__setImageWithURL(require('NSURL').URLWithString('https://onevcat.com/assets/images/avatar.jpg'));

###Btn添加点击事件
		
		btn.addTarget_action_forControlEvents(self, "handleBtn:", 1 << 6);
		handleBtn: function(sender) {
        console.log('这是动态添加的按钮响应事件')
    	},
 
###复制到剪切板
		
		 var pasteboard = require('UIPasteboard').generalPasteboard();
		  pasteboard.setString('这是动态添加的按钮响应事件');
		  
###三方弹框 
		
		   require('MBProgressHUD').showSuccess_toView("复制成功", null);
		   

###pop出页面
		
		   self.navigationController().popViewControllerAnimated(YES);
		   
###push 到相应的页面
		
		  var safeVC = require('PTSafeViewController').alloc().init();
		  self.navigationController().pushViewController_animated(safeVC, YES);

##修复数据	  
		
###NSUserDefaults 本地存储
		require('NSUserDefaults').standardUserDefaults().setObject_forKey("123", "456");
		var dic = require('NSUserDefaults').standardUserDefaults().objectForKey("456");
		console.log(dic)  

###取本地模型的数据(全局模型)
		
		 var str = self.agentModel().myQQPopularizeUrl();
		 console.log('model*******',str);

###动态新增属性字段
		defineClass("JPTableViewController", ['data', 'totalCount'], {
		  init: function() {
		     self = self.super().init()
		     self.setData(["a", "b"])     //添加新的 Property (id data)
		     self.setTotalCount(2)
		     return self
		  },
		  viewDidLoad: function() {
		     var data = self.data()     //获取 Property 值
		     var totalCount = self.totalCount()
		  },
		})

###加载动态库（插件化）
	
		var bundle = NSBundle.bundleWithPath("/System/Library/Frameworks/SafariServices.framework");
	bundle.load();


#修复调用方法defineClass重写该方法
	
		require("NSArray,UIView, UIColor'");
		defineClass("PTHomeViewController", {
    		testFunction: function() {
        	self.setArr([ "熊猫", "🐼", "熊猫棋牌" ]);
        	var str = self.arr().objectAtIndex(2);
        	console.log("个人中心页面JSPatch调用" , str);
    		}
		}, {});
		

-----

##warning
		
		1.JS不区分整数和浮点数。解析字典以后的value不需要通过 floatValue等方法转换，而是自动就转换成对应的数据类型。
		2.nil在JSPatch中 不能使用，如果是用if（a == nil）应该用if（!a）来代替。
		3.self.view.setFrame（{x:0,y:0,width:100,height:100}); 设置frame必须这种格式，如果是CGSize那么就在括号里写上{width：100,height:100}。当我们需要获得全屏的宽度的时候我们需要怎么做呢？var tempScreenHeight = UIScreen.mainScreen().bounds().height 明显可以看到 他与我们平常相比 bounds之后 可以直接获取到height 而不是 size.height这个需要注意。
		4.== 在JSPatch中只能比较基本数据类型，遇到自己写的类 或者model是无法比较的。
		5.C底层的方法在JSPatch中不能直接调用，宏如果想要调用，1.如果没有与C有关的语句可以直接写一个函数方法进行调用。2.举例如下：require(’JPEngine’).addExtensions([‘XXX’])增加拓展
		6.首先从 OC 返回的 NSArray / NSDictionary 对象是不能直接用 for...in 遍历的，需要调用 .toJS()， toJS是它给的一个接口，把OC对象转成JS对象。
		7.在OC中我们会使用 Arr[100]，来获得 数组的101位，而在js中如果你是OC代码中的数组则需要 objectAtIndex(i)；如果你是在JS中自己var a = [1,2,3]，那么你要拿到他的数目你要用的是 a.length，但是 如果是OC转过来的数组 则需要用 a.count()；如果 OC的使用了length那么数目永远返回0，如果 JS使用count是会报错的。
		8.我们平常用的NSString 的format方法 在JS中 可以直接用+连接，比如 var C = ’A’ + ‘B’；
		如果遇到不是str的可以用String(x)的方式来转成str类型。
		9.在里面使用Block的时候要注意 不能使用self。如果你要用需要先在外面var slf = self；否则是会报错的。
		10.我们在用一些方法如tableview initWithStyle_reuseIdentifier 我们要注意 style是枚举，往往是str我们需要用单引号或者双引号括起来。或者直接用数字来表示。
		
	
##测试源码（远端下发）

	require("NSArray,UIView, UIColor,NSURL");

	defineClass("PTHomeViewController", {
	    testFunction: function() {
	        self.setArr([ "熊猫", "🐼", "熊猫棋牌" ]);
	        var str = self.arr().objectAtIndex(2);
	        console.log("个人中心页面JSPatch调用" , str);
	    }
	}, {});
	
	
	defineClass("PTAgentViewController", {
	    viewDidLoad: function() {
	        self.super().viewDidLoad();
	        self.setUpUI();
	        self.initWebData();
        
        self.initBtn();
        self.initView();
        
       
        console.log("代理页面viewDidLoad JSPatch调用");
    },
    handleBtn: function(sender) {
        console.log('这是动态添加的按钮响应事件')
        var pasteboard = require('UIPasteboard').generalPasteboard();
        pasteboard.setString('这是动态添加的按钮响应事件');
        require('MBProgressHUD').showSuccess_toView("复制成功", null);

    },
    initBtn: function() {
            var width = require('UIScreen').mainScreen().bounds().width;
            var heigth = require('UIScreen').mainScreen().bounds().height;
            var btn = require('UIButton').alloc().initWithFrame({x:000, y:(heigth-350), width:300, height:150});
            btn.setTitle_forState('这个按钮是通过JSPatch动态添加上去的啊', 0);
            btn.addTarget_action_forControlEvents(self, "handleBtn:", 1 << 6);
            btn.setBackgroundColor(require('UIColor').grayColor());
            self.myAgentView().addSubview(btn);
    },
    initView: function() {
            var width = require('UIScreen').mainScreen().bounds().width;
            var heigth = require('UIScreen').mainScreen().bounds().height;
            var v = require('UIImageView').alloc().initWithFrame({x:200, y:(heigth-350), width:300, height:150});
            self.myAgentView().addSubview(v);
            v.sd__setImageWithURL(require('NSURL').URLWithString('https://onevcat.com/assets/images/avatar.jpg'));
            
    },
    initWebData: function() {
        console.log("代理页面 JSPatch调用");
        self.getMyAgentInfo();
       
    }
	    
	}, {});



...未完待续


                    编译library的脚本


                    #!/bin/sh

                    #要build的target名
                    target_Name=${PROJECT_NAME}
                    if [[ $1 ]]
                    then
                    target_Name=$1
                    fi

                    UNIVERSAL_OUTPUT_FOLDER="${SRCROOT}/${PROJECT_NAME}_Products"

                    # 创建输出目录，并删除之前的文件
                    rm -rf "${UNIVERSAL_OUTPUT_FOLDER}"
                    mkdir -p "${UNIVERSAL_OUTPUT_FOLDER}"

                    # 分别编译真机和模拟器版本
                    xcodebuild -target "${target_Name}" ONLY_ACTIVE_ARCH=NO -configuration ${CONFIGURATION} -sdk iphoneos  BUILD_DIR="${BUILD_DIR}" BUILD_ROOT="${BUILD_ROOT}" clean build
                    xcodebuild -target "${target_Name}" ONLY_ACTIVE_ARCH=NO -configuration ${CONFIGURATION} -sdk iphonesimulator BUILD_DIR="${BUILD_DIR}" BUILD_ROOT="${BUILD_ROOT}" clean build

                    #复制头文件到目标文件夹
                    HEADER_FOLDER="${BUILD_DIR}/${CONFIGURATION}-iphonesimulator/include/${target_Name}"
                    if [[ -d "${BUILD_DIR}/${CONFIGURATION}-iphonesimulator/usr/local/include" ]]
                    then
                        HEADER_FOLDER="${BUILD_DIR}/${CONFIGURATION}-iphonesimulator/usr/local/include"
                    fi
                    cp -R "${HEADER_FOLDER}" "${UNIVERSAL_OUTPUT_FOLDER}"

                    #合成模拟器和真机.a包
                    lipo -create "${BUILD_DIR}/${CONFIGURATION}-iphonesimulator/lib${target_Name}.a" "${BUILD_DIR}/${CONFIGURATION}-iphoneos/lib${target_Name}.a" -output "${UNIVERSAL_OUTPUT_FOLDER}/lib${target_Name}.a"

                    # 判断build文件夹是否存在，存在则删除
                    if [ -d "${SRCROOT}/build" ]
                    then
                    rm -rf "${SRCROOT}/build"
                    fi

                    #打开目标文件夹
                    open "${UNIVERSAL_OUTPUT_FOLDER}"








                    编译framework的shell脚本
                    
                    


                    #!/bin/sh
                    #要build的target名
                    TARGET_NAME=${PROJECT_NAME}
                    if [[ $1 ]]
                    then
                    TARGET_NAME=$1
                    fi
                    UNIVERSAL_OUTPUT_FOLDER="${SRCROOT}/${PROJECT_NAME}_Products/"

                    #创建输出目录，并删除之前的framework文件
                    mkdir -p "${UNIVERSAL_OUTPUT_FOLDER}"
                    rm -rf "${UNIVERSAL_OUTPUT_FOLDER}/${TARGET_NAME}.framework"

                    #分别编译模拟器和真机的Framework
                    xcodebuild -target "${TARGET_NAME}" ONLY_ACTIVE_ARCH=NO -configuration ${CONFIGURATION} -sdk iphoneos BUILD_DIR="${BUILD_DIR}" BUILD_ROOT="${BUILD_ROOT}" clean build
                    xcodebuild -target "${TARGET_NAME}" ONLY_ACTIVE_ARCH=NO -configuration ${CONFIGURATION} -sdk iphonesimulator BUILD_DIR="${BUILD_DIR}" BUILD_ROOT="${BUILD_ROOT}" clean build

                    #拷贝framework到univer目录
                    cp -R "${BUILD_DIR}/${CONFIGURATION}-iphonesimulator/${TARGET_NAME}.framework" "${UNIVERSAL_OUTPUT_FOLDER}"

                    #合并framework，输出最终的framework到build目录
                    lipo -create -output "${UNIVERSAL_OUTPUT_FOLDER}/${TARGET_NAME}.framework/${TARGET_NAME}" "${BUILD_DIR}/${CONFIGURATION}-iphonesimulator/${TARGET_NAME}.framework/${TARGET_NAME}" "${BUILD_DIR}/${CONFIGURATION}-iphoneos/${TARGET_NAME}.framework/${TARGET_NAME}"

                    #删除编译之后生成的无关的配置文件
                    dir_path="${UNIVERSAL_OUTPUT_FOLDER}/${TARGET_NAME}.framework/"
                    for file in ls $dir_path
                    do
                    if [[ ${file} =~ ".xcconfig" ]]
                    then
                    rm -f "${dir_path}/${file}"
                    fi
                    done

                    #判断build文件夹是否存在，存在则删除
                    if [ -d "${SRCROOT}/build" ]
                    then
                    rm -rf "${SRCROOT}/build"
                    fi

                    rm -rf "${BUILD_DIR}/${CONFIGURATION}-iphonesimulator" "${BUILD_DIR}/${CONFIGURATION}-iphoneos"

                    #打开合并后的文件夹
                    open "${UNIVERSAL_OUTPUT_FOLDER}"

                    6人点赞
                    iOS


                    作者：Ro_bber
                    链接：https://www.jianshu.com/p/fffc55967f70
                    来源：简书
                    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。




