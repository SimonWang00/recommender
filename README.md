# recommender

### 推荐模型简介
- 目标：有三款产品某企通、某赋通和某票，通过推荐提高用户群体从某企通和某票到某赋通产品的转化率。
- 数据情况：用户数据体量，某企通：某赋通：某票 = 100 ：10 ：1
- 推荐算法选型：试验过当下十分流行的Item_CF和User_CF，产生的推荐效果并不理想，具体过程如下：
<img src="./pictures/算法选型.png?raw=true"/> 
- 推荐模型：选择了RFM模型、决策树模型和专业运营人员的经验知识，具体的推荐架构如下：
<img src="./pictures/推荐架构.png?raw=true"/> 

### 购买某赋通的数学期望
- 核心思想：将某企通的用户通过Kmeans聚类进行分群，跑手肘法使分层数依次为2、3、4....10。分别计算相应层数中，
每个群体购买某赋通的数学期望，目标是找出获得最大数学期望的群体，进行画像推荐。
- 用户分群的效果：随着分群的种类不断增加，用户购买某赋通的数学期望如下所示：
<img src="./pictures/手肘法.png?raw=true"/>
<img src="./pictures/某赋通数学期望.png?raw=true"/> 
- 结论：可以看出购买某赋通的数学期望偏低，这也同样证明了协同过滤推荐算法的不适用，因为数据在向未购买的用户群靠拢，
所以需要解决购买与不购买数据样本不平衡的问题。

### 解决思路
选择了非常弱的分类器决策树，参考传统的RFM模型，进行用户推荐。

### 环境
- Windows 10
- Python 3.6.5

### 依赖包
```
pip install -r requirements.txt
```

### 程序执行
```
python recommender.py
```

### 建模过程
- 特征工程：
 - 数据清洗：对文本型数据、数值型数据、时间型数据和确实数据进行清洗，一致性检查和业务逻辑检查
 - 特征选择：相关性和重要性计算。
    <img src="./pictures/特征相关性计算.png?raw=true"/> <img src="./pictures/特征重要性计算.png?raw=true"/> <img src="./pictures/特征累计重要性计算.png?raw=true"/>
- 用户画像：
 - 基于到期时间的推荐：依次推荐给快到期用户续费使用；
 - 基于效用的推荐：开票量、开票金额和登录使用次数都是构成效用的重要指标；
 - 基于RFM用户价值模型的推荐：对消费金额和消费频次高的用户适时产生推荐；
 - 混合推荐：现实应用中，其实很少有直接用某种算法来做推荐的系统。通过给不同算法的结果加权重来综合结果，
 或者是在不同的计算环节中运用不同的算法来混合，达到更贴合自己业务的目的。
- 推荐引擎
 - 决策树：不确定性的计算采用的是基尼系数，之前已经计算过累计重要性，所以这里就不剪枝。
 <img src="./pictures/决策树.png?raw=true"/> 
 - RFM模型：通过不断调整权重，运营人员认为如下公式比较符合预期。computeTotalScore。
 ```
def computeTotalScore(scoreDic):
    '''
    根据用户对所有商品的打分
    :param scoreDic:每个用户对所有商品的评级
    :return:对产品的打分
    index = ["times-wp","je-wp","recently-wp","times-bqt","je-bqt","recently-bqt","times-bft","je-bft","recently-bft","dayLoginTimes",
         "zczb","industry","ages","dayInvoiceNum","dayInvoiceJe"]
    '''
    if len(scoreDic) <1:raise Exception('scoreDic is none')
    if scoreDic.get('dayLoginTimes') == None:scoreDic['dayLoginTimes'] = 0
    score_common = scoreDic['registeredCapital'] * 10 + scoreDic['dayCountAvg'] * 30 + scoreDic['loginFrequency'] * 30 + \
            scoreDic['daySumAvg'] * 30 + scoreDic['dateOfEstablishment'] * 10 + scoreDic['industry'] * 10
    if scoreDic['deadline']==5: bft = 200 + (scoreDic['userConsumeTotalAmount'] + scoreDic['userConsumeTotalTimes'])* 50
    else:bft = 0
    if scoreDic['recently_bqt']==5: bqt = 100 + (scoreDic['je_bqt'] + scoreDic['times_bqt'])* 50
    else:bqt = 0
    if scoreDic['deadline_wp']==5: wp = 100 + (scoreDic['je_wp'] + scoreDic['times_wp'])* 50
    else:wp = 0
    score = bft + bqt + wp + score_common
    return score
```

### 优化空间
1、加大力度对用户数据的采集；
2、根据最近几次推荐的反馈结果，对模型进行优化；
3、搭建实时的用户推荐系统，后期我会陆续更新基于Mahout的推荐系统代码。
