$(document).ready(function() {

    //判断路劲 执行默认加载1小时数据
    if (window.location.pathname == "/"){post_charts_data(1, '', '','','')};

    $("#make_charts").click(function() {
        var start_query = $("#start_query").val();
        var end_query = $("#end_query").val();

	var statusa =jQuery("#ssss").attr('aria-expanded'); 

 	if (statusa === 'true'){
            var client_address = $("#client_address").val() ;
            var http_urlinterface = $("#http_urlinterface").val();
	    if (client_address){
                if ( !checkIP(client_address)) {return  ;}
            }
	}

        if (! start_query) {
            swal('请选择开始时间!!!!');
            return
        };
        if (! end_query) {
            swal('请选择结束时间!!!!');
            return
        };

        var range = GetDateDiff($("#start_query").val(), $("#end_query").val(), "hour");

        if(range < 0){swal('结束时间比开始时间小，请重新选择!!'); return};
        (range > 24) ? swal("查询时间间隔不能大于1天") : post_charts_data(range, start_query, end_query,client_address ,http_urlinterface);
    });

    $("#one_hour").click(function() {

        var statusa =jQuery("#ssss").attr('aria-expanded');

        if (statusa === 'true'){
            var client_address = $("#client_address").val() ;
            var http_urlinterface = $("#http_urlinterface").val();
            if (client_address){
                if ( !checkIP(client_address)) {return  ;}
            }
            post_charts_data(1, '', '',client_address ,http_urlinterface);
        }else{
            post_charts_data(1, '', '','','');
	  }
    });
    $("#five_hours").click(function() {

        var statusa =jQuery("#ssss").attr('aria-expanded');

        if (statusa === 'true'){
            var client_address = $("#client_address").val() ;
            var http_urlinterface = $("#http_urlinterface").val();
            if (client_address){
                if ( !checkIP(client_address)) {return  ;}
            }
            post_charts_data(5, '', '',client_address ,http_urlinterface);
        }else{
            post_charts_data(5, '', '','','');
	  }
    });
    $("#one_day").click(function() {

        var statusa =jQuery("#ssss").attr('aria-expanded');

        if (statusa === 'true'){
            var client_address = $("#client_address").val() ;
            var http_urlinterface = $("#http_urlinterface").val();
            if (client_address){
                if ( !checkIP(client_address)) {return  ;}
            }
            post_charts_data(24, '', '',client_address ,http_urlinterface);
        }else{
            post_charts_data(24, '', '','','');
	   }
    });

    function GetDateDiff(startTime, endTime, diffType) {
        startTime = startTime.replace(/\-/g, "/");
        endTime = endTime.replace(/\-/g, "/");

        diffType = diffType.toLowerCase();
        var sTime = new Date(startTime); //开始时间
        var eTime = new Date(endTime); //结束时间
        var divNum = 1;
        switch (diffType) {
        case "second":
            divNum = 1000;
            break;
        case "minute":
            divNum = 1000 * 60;
            break;
        case "hour":
            divNum = 1000 * 3600;
            break;
        case "day":
            divNum = 1000 * 3600 * 24;
            break;
        default:
            break;
        }
        return parseInt((eTime.getTime() - sTime.getTime()) / parseInt(divNum));
    }

    function post_charts_data(hours, starttime, endtime, client_address ,http_urlinterface ) {
        var charts_condition = $("#charts_condition option:selected").text();
	var allow_app = getUrlParam('allow_app');

        $.post("/perf/interface/", {
            server_name: charts_condition,
            starttime: starttime,
            endtime: endtime,
            range: hours, //单位为小时
	    client_address: client_address,
	    http_urlinterface: http_urlinterface,
	    allow_app: allow_app
        },
        function(datas) {
            dddd(datas, charts_condition,client_address ,http_urlinterface);
	    chinamap(datas['china_data']);

	    var china_obj = datas['china_data'] ;
            if (window.localStorage.getItem("area_average")){window.localStorage.removeItem("area_average")}
	    var  c_arr = [] ;


	    $.each(china_obj,function(index,value){
		
		c_arr.push([value.name, value.value]);		

	    });


            window.localStorage.setItem('area_average',c_arr);
		
	    apm_pv(datas['area_pv']);
            //存储数据为本地,供大图使用 
            if (window.localStorage.getItem("area_pv")){window.localStorage.removeItem("area_pv")}
            window.localStorage.setItem('area_pv',datas['area_pv']);
	    $("#new_link").removeClass("hide");
	    $("#new_link2").removeClass("hide");

        });

    };

    function dddd(datas, charts_condition, client_address ,http_urlinterface) {
	var allow_app = getUrlParam('allow_app');
        var result = datas['msg'];
        var title = {
            text: charts_condition + '请求分布展示'
        };

        var chart = {
            type: 'spline'
        };

        var xAxis = {
            labels: {
                enabled: false
            },
            'categories': result['categories']

        };

        var exporting = {
	    enabled:false
        };


        var plotOptions = {
            spline: {
                marker: {
                    enabled: true
                }
            },

            series: {
                cursor: 'pointer',
                events: {
                    click: function(event) {
                        if (this.name.indexOf('0-1s') != -1) {
                            var series_type = '1000'
                        };
                        if (this.name.indexOf('1-2s') != -1) {
                            var series_type = '2000'
                        };
                        if (this.name.indexOf('2-3s') != -1) {
                            var series_type = '3000'
                        };
                        if (this.name.indexOf('>3s') != -1) {
                            var series_type = '3001'
                        };
                        location.href = '/chartsdetail/?serverName=' + charts_condition + '&type=' + series_type + '&endTime=' + event.point.category +"&allow_app=" + allow_app + '&c_ip=' + client_address +'&requesturl=' + http_urlinterface + '&page=1';

                    }
                }
            }

        };

        var credits = {
            enabled: false //不显示LOGO 
        };

        var series = result['data'];

        var json = {};

        json.title = title;
        json.credits = credits;
        json.chart = chart;
        json.xAxis = xAxis;
        json.plotOptions = plotOptions;
        json.series = series;
        json.exporting = exporting;
        $('#pinpoint-container').highcharts(json);
    };


////////////


    //解析IP
    
    var count = 0;
    var firstTime = 0;
    var SecondTime = 0;
    var flag = true;
    
    $("#dns_ip td").click(function() {
    
        var col = $(this).index();
        if (col == 0) {
        var date = new Date();
        var seconds = date.getTime();
        if (flag) {
            firstTime = seconds;
            flag = false;
        } else {
            SecondTime = seconds;
            flag = true;
        }
    
        if (SecondTime == 0) {
            count++;
                var ip = $(this).parent().find("td:first").text();
                $.post("/getIpInfo/", {
                    ip: ip
                },
                function(data, status) {
                        swal(data + "来源:  " + "数据来源于淘宝IP地址库");
                });
    
    
        } else {
            if (Math.abs(SecondTime - firstTime) > 5000) {
                count++;
                    var ip = $(this).parent().find("td:first").text();
                    $.post("/getIpInfo/", {
                        ip: ip
                    },
                    function(data, status) {
                        swal(data + "来源:  " + "数据来源于淘宝IP地址库");
                    });
    
    
            } else {
                swal("IP解析频率太频繁，,请在5s后再试！！");
            }
        }
	}
    
    });



///////// pinpoint  js
    $("#get_top20").click(function() {
	var  ppstarttime = $("#ppstarttime").val() ;
        var  ppendtime  = $("#ppendtime").val() ;
	var  pinpoint_name = $("#pp_select option:selected").val();

        var range = GetDateDiff(ppstarttime, ppendtime, "second");
        if(range < 0){swal('结束时间比开始时间小，请重新选择!!'); return};




	$("#pp_tbody").empty();
	if (pinpoint_name){

	 $.post("/pinpoint/", {
		p_name : pinpoint_name,
                ppstarttime: ppstarttime,
	   	ppendtime: ppendtime
        },
        function(datas) {
            var data = datas['msg'];

	    if (data){
	            $('.bootstrapTable').bootstrapTable('load',{
		        data: data
			});



		}else{
		    swal("最近5分钟没有数据!!!!");
	            $('.bootstrapTable').bootstrapTable('removeAll');
		}

        });
	}

    });



//获取URL参数函数
//
    function getUrlParam(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
        var r = window.location.search.substr(1).match(reg);  
        if (r != null) return unescape(r[2]); return null; 
    }




});



