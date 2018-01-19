function chinamap(china_data) {
    var dom = document.getElementById("china-container");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;


    option = {
        title: {
            text: '全国访问平均时间分布图',
	    subtext: '单位(ms)',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        visualMap: {
            min: 0,
            max: 2500,
            left: 'left',
            top: 'bottom',
            text: ['高', '低'],
            // 文本，默认为数值文本
            calculable: true
        },
        series: [{
            name: '平均值',
            type: 'map',
            mapType: 'china',
            roam: false,
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data: china_data  
        }]
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}







function  apm_pv(data){
    $('#apmpv_container').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '全国访问APM接口PV图'
        },
	exporting: {
	     enabled:false
	},
        xAxis: {
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'pv (次数)'
            }
        },
        series: [{
            name: 'APM_PV',
            data: data , 
        }]
    });
};






function  all_pv(data){
    $('#allpv_container').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '全国访问APM接口PV图'
        },
        xAxis: {
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'pv (次数)'
            }
        },
        series: [{
            name: 'APM_PV',
            data: data ,
        }]
    });
};



//查看大图
function china_bigmap(china_data) {
    var dom = document.getElementById("china_bigcontainer");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;


    option = {
        title: {
            text: '全国访问平均时间分布图',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        visualMap: {
            min: 0,
            max: 2500,
            left: 'left',
            top: 'bottom',
            text: ['高', '低'],
            // 文本，默认为数值文本
            calculable: true
        },
        series: [{
            name: '平均值',
            type: 'map',
            mapType: 'china',
            roam: false,
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data: china_data  
        }]
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}

