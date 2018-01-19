var setting = {
    callback: {
        onClick: onClick
    }
};

function onClick(event, treeId, treeNode, clickFlag) {
    $('#zk_tree').attr("value", get_parent_tree());
    $('#zk_name').attr("value", treeNode.name);
    var $name = $("#select_list option:selected").text();
    $('#default_cluster_name').attr("value", $name);
}

function get_parent_tree() {
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getSelectedNodes();
    treeNode = nodes[0];
    var value_data = treeNode.name;

    if (value_data.indexOf("/") != 0) {

        var sNodes = treeObj.getSelectedNodes();
        if (sNodes.length > 0) {
            var node = sNodes[0].getParentNode();
            console.log(node.name);
            console.log(value_data);
            if (node.name == "/") {
                var value_data = '/' + value_data;
            } else {
                var value_data = node.name + '/' + value_data;
            }
        }
    }
    return value_data
}

$(document).ready(function() {

    function load_node_tree() {
        var $name = $("#select_list option:selected").text();
        if ($("#node_path").val() == "") {
            alert("输入首节点路劲");
        } else {
            $.post("/node_path/", {
                node_path: $("#node_path").val(),
                cluster_name: $name,
            },
            function(data) {
		//过滤脏数据
		if (data.length < 10 ){
		    alert(data);
		}else{
                $.fn.zTree.init($("#treeDemo"), setting, JSON.parse(data));
		}


            });
        };
    }

    ////////////////////////
    $("#node_search").click(function() {
        load_node_tree();
    });
    ////////////////////////
    //
    $("#delete_btn").click(function() {

        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        var $name = $("#select_list option:selected").text();
        treeNode = nodes[0];
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
            var result = post_func($name, get_node_tree());
            if (String(result) != "false") {
                // for (var i = 0,l = nodes.length; i < l; i++) {
                //     treeObj.removeNode(nodes[i]);
                // }
                load_node_tree();
            }
        }

    });
    //////////////////////
    //需要获取函数里的函数的返回值,待改动
    function post_func($name, node) {
        var msg = "确定要删除吗?";
        if (confirm(msg) == true) {
            $.post("/post_delete/", {
                node_key: node,
                cluster_name: $name,
            },
            function(data) {
                alert(data);
                if (data == "无法删除节点") {
                    return false;
                }

            });
        } else {
            return false;
        }
    }

    ////////////////////////
    $("#value_info").click(function() {

        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        var name = $("#select_list option:selected").text();
        treeNode = nodes[0];
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
            var value_data = get_node_tree();
            if (value_data == "/") {
                alert("根节点下无数据");
            } else {
                $.post("/get_node_value/", {
                    choose_node: value_data,
                    cluster_name: name,
                },
                function(data) {
                    if (data == "") {
                        var data = "此节点下没有值"
                    }
                    $('#display_value').text(data);
                    $('#check_info_myModal').modal('show');

                });
            };
        };
    });

    /////////////////////////////////////////
    function get_node_tree() {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];

        var value_data = treeNode.name;
        if (value_data.indexOf("/") != 0) {

            var sNodes = treeObj.getSelectedNodes();
            if (sNodes.length > 0) {
                var node = sNodes[0].getParentNode();
                if (node.name == "/") {
                    var value_data = '/' + value_data;
                } else {
                    var value_data = node.name + '/' + value_data;
                }
            }
        }
        return value_data
    }
    ////////////////////////////////////////////
    $("#value_change").click(function() {

        var value_data = get_node_tree();
        var $name = $("#select_list option:selected").text();
        if (value_data == "/") {
            alert("根节点不能修改");
        } else {

            $.post("/get_node_value/", {
                cluster_name: $name,
                choose_node: value_data,
            },
            function(data) {
                $('#node_name').attr("value", get_node_tree());
                //$('#node_value').attr("value", data);
                $('#textarea_node_value').html(data);
                $('#myModal').modal('show');

            });

        };
    });
    ////////////////////////////////////////////
    $("#commit_btn").click(function() {
        var node_name = $('#node_name').attr("value");
        var node_value = $('#textarea_node_value').val();
        var $name = $("#select_list option:selected").text();

        $.post("/mod_node_value/", {
            node_name: node_name,
            node_value: node_value,
            cluster_name: $name,
        },
        function(data) {
            alert(data);
            $('#myModal').modal('hide');
                location.reload(true);
            //load_node_tree();
        });

    });
    ////////////////////////////////////////////
    $("#value_add").click(function() {
        $('#parent_node_name').attr("value", get_node_tree());
        $('#myModal_add').modal('show');
        $('#new_node_name').val("");
        $('#new_node_value').val("");
        var new_node_name = $('#new_node_name').val();
        var new_node_value = $('#new_node_value').val();
    });
    ////////////////////////////////////////////
    $("#value_post").click(function() {
        var node_name = $('#parent_node_name').attr("value");
        var new_node_name = $('#new_node_name').val();
        var new_node_value = $('#new_node_value').val();
        var $name = $("#select_list option:selected").text();
        if (node_name != "/") {
            var New_post_node = node_name + "/" + new_node_name;
        } else {
            var New_post_node = "/" + new_node_name;

        }
        if (new_node_name == "") {
            alert("新节点名必须增加");
        } else {
            $.post("/add_node/", {
                New_post_node: New_post_node,
                new_node_value: new_node_value,
                cluster_name: $name,
            },
            function(data) {
                alert(data);
                $('#myModal_add').modal('hide');
                load_node_tree();

            });
        }

    });
    ////////////////////////////////////////////
    $("#batch_xiugai").click(function() {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];

        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
	 $('#firstkey').empty();
         $('#secondkey').empty();
         $('#thirdkey').empty();
         $('#fourthkey').empty();
         $('#fifthkey').empty();
         $('#firstvalue').empty();
         $('#secondvalue').empty();
         $('#thirdvalue').empty();
         $('#fourthvalue').empty();
         $('#fifthvalue').empty();
        var $name = $("#select_list option:selected").text();
        $('#myModal_batch').modal('show');
        $('#add_node_name').attr("value", get_node_tree());
        $('#add_cluster_name').attr("value", $name);
	}
    });
    ////////////////////////////////////////////
    $("#batch_delete").click(function() {

        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var sNodes = treeObj.getSelectedNodes();
        if (sNodes.length > 0) {
            var isParent = sNodes[0].isParent;
            if (String(isParent) != "false") {
                var value_data = get_node_tree();

                var result = post_batch_delete(value_data);

                if (String(result) != "false") {
                    load_node_tree();
                }

            } else {
                alert("该节点为子节点,批量删除请选择父节点");
            };
        } else {
            alert("请先选择一个节点");
            return;
        };

    });
    //////////////////////
    function post_batch_delete(node) {
        var msg = "确定要删除吗?";
        var $name = $("#select_list option:selected").text();
        if (confirm(msg) == true) {
            var res_msg = $.post("/batch_delete/", {
                node_key: node,
                cluster_name: $name,
            },
            function(data) {
                alert(data);
            });
            return res_msg;
        } else {
            return false;
        }
    }
    //////////////////////
    $("#check_snapshot").click(function() {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
            var value_data = get_node_tree();

            $.post("/validate_snapshot/", {
                node_key: value_data,
            },
            function(data) {
                if (data == "OK") {

                    location.href = '/check_snapshot/key_node=' + value_data + "/";
                } else {
                    alert("此节点下没有快照!!!!!!");

                }

            });

        }
    });
    //////////////////////
    $("#make_snapshot").click(function() {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
            var curr_node = get_node_tree();
            MAKE_SNAPSHOST(curr_node);
        }
    });
    //////////////////////
    function MAKE_SNAPSHOST(node) {
        var msg = "确定要生成地节点的快照吗?";
        var $name = $("#select_list option:selected").text();
        if (confirm(msg) == true) {
            var res_msg = $.post("/m_snapshot/", {
                node_tree: node,
                cluster_name: $name,
            },
            function(data) {
                alert(data);
            });
            return res_msg;
        } else {
            return false;
        }
    }
    //////////////////////
    $("#batch_snapshot").click(function() {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getSelectedNodes();
        treeNode = nodes[0];
        if (nodes.length == 0) {
            alert("请先选择一个节点");
            return;
        } else {
            var curr_node = get_node_tree();
            BATCH_SNAPSHOST(curr_node);
        }
    });
    //////////////////////
    function BATCH_SNAPSHOST(node) {
        var msg = "确定要批量生成次节点下所有子节点的快照吗?";
        if (confirm(msg) == true) {
            var $name = $("#select_list option:selected").text();
            var res_msg = $.post("/batch_m_snapshot/", {
                node_tree: node,
                cluster_name: $name,
            },
            function(data) {
                alert(data);
            });
            return res_msg;
        } else {
            return false;
        }
    }
    //////////////////////
    $("#sync_case").click(function() {
        alert("功能开发中....");
    });
    //////////////////////
    $("#import").click(function() {
        alert("功能开发中.....");
    });
    //////////////////////
    $("#add_host").click(function() {
        $('#add_host_modal').modal('show');
    });
    //////////////////////
    $("#AddHost_btn").click(function() {
        var cluster_name = $('#cluster_name').val();
        var cluster_conf = $('#cluster_conf').val();
        var cluster_lable = $('#cluster_lable').val();

        if (cluster_name == "" || cluster_conf == "") {
            alert("集群名称或者配置不能为空");
        } else {
            $.post("/cluster_operation/", {
                cluster_conf: cluster_conf,
                cluster_name: cluster_name,
                cluster_lable: cluster_lable,
                operation: "cluster_add",
            },
            function(data) {
                alert(data);
            });
            location.href = '/zk_page/';
        };

    });
    //////////////////////
    $("#delete_host").click(function() {
        var $radio = $("#table input:radio:checked").parent().parent().parent();
        var $row = parseInt($radio.index()) + 1;
        var $c_name = $("#table tr:eq(" + $row + ") td:nth-child(1)").html();
        if ($c_name == null) {
            alert("没有要删除的主机!!!!!");
        } else {
            delete_cluster($c_name);
        }
    });

    //////////////////////////////
    function delete_cluster($c_name) {
        var msg = "确定要删除吗?";
        if (confirm(msg) == true) {
            $.post("/cluster_operation/", {
                cluster_name: $c_name,
                operation: "cluster_delete",
            },
            function(data) {
                alert(data);
            });
            location.href = '/zk_page/';
        } else {
            return false;
        }
    }
    //////////////////////
    $("#batch_value_post").click(function() {
        var $key1 = $('#firstkey').val();
        var $key2 = $('#secondkey').val();
        var $key3 = $('#thirdkey').val();
        var $key4 = $('#fourthkey').val();
        var $key5 = $('#fifthkey').val();
        var $value1 = $('#firstvalue').val();
        var $value2 = $('#secondvalue').val();
        var $value3 = $('#thirdvalue').val();
        var $value4 = $('#fourthvalue').val();
        var $value5 = $('#fifthvalue').val();
    
        node_data = new Object();
        if ($key1 != "") {
            node_data.node1 = [$key1, $value1]
        }
        if ($key2 != "") {
            node_data.node2 = [$key2, $value2]
    
        }
        if ($key3 != "") {
            node_data.node3 = [$key3, $value3]
    
        }
        if ($key4 != "") {
            node_data.node4 = [$key4, $value4]
    
        }
        if ($key5 != "") {
            node_data.node5 = [$key5, $value5]
    
        }
    
        obj_json = $.toJSON(node_data);
        //document.write(obj_json);
        if ($(node_data).length == 0){
            alert("请填写要增加的节点!!!!!")
	}else{
            var name = $("#select_list option:selected").text();
            $.post("/batch_node_json/", {
                node_json: obj_json,
		cluster_name: name,
		current_node:get_node_tree(),
            },                                                                                                                                        
            function(data) {   
		alert(data);
                $('#myModal_batch').modal('hide');
                load_node_tree();
                                                                                                                                                      
            });	   

	}
    
    });

    //////////////////////
    $('#history_snapshot').on('click', 'button[id*=snapshot_delete]',delete_id);
    function delete_id() {
        var $this = $(this);
        var $history_id = $this.closest('tbody').find('tr#history_id');
        var index = ($history_id.index($this.closest('tr#history_id')[0])) + 1;
        var $id = $("#history_snapshot tr:eq(" + index + ") td:nth-child(1)").html();
            $.post("/snapshot_delete/", {
               snapshot_id: $id,
            },
            function(data) {
                alert(data);
                location.reload(true);

            })
    }


    //////////////////////
    $('#history_snapshot').on('click', 'button[id*=rollback]',rollback_id)
    function rollback_id() {
        var $this = $(this);
        var $history_id = $this.closest('tbody').find('tr#history_id');
        var index = ($history_id.index($this.closest('tr#history_id')[0])) + 1;
        var $id = $("#history_snapshot tr:eq(" + index + ") td:nth-child(1)").html();
        
	var msg = "确定要回滚吗?";
        if (confirm(msg) == true) {
            $.post("/snapshot_rollback/", {
               snapshot_id: $id,
            },
            function(data) {
                alert(data);
                location.reload(true);

            });
        } else {
            return false;
        }



    }



    //////////////////////
    $("#modfi_host").click(function() {
        var $radio = $("#table input:radio:checked").parent().parent().parent();
        var $row = parseInt($radio.index()) + 1;
        var $c_name = $("#table tr:eq(" + $row + ") td:nth-child(1)").html();

            $.post("/cluster_operation/", {
                cluster_name: $c_name,
                operation: "cluster_modefi",
            },
            function(data) {
		$('#new_cluster_id').attr("value", data.id);
		$('#new_cluster_name').attr("value", data.cluster_name);
		$('#new_cluster_conf').attr("value", data.hosts);
		$('#new_cluster_lable').attr("value", data.business);
		$('#modfiy_host_modal').modal('show');
                console.log(data.hosts);
            });

    });
    //////////////////////
        $("#modfiy_zk_cluster").click(function() {
        var new_cluster_id = $('#new_cluster_id').val();
        var new_cluster_name = $('#new_cluster_name').val();
        var new_cluster_conf = $('#new_cluster_conf').val();
        var new_cluster_lable = $('#new_cluster_lable').val();

        if (new_cluster_name == "" || new_cluster_conf == "") {
            alert("集群名称或者配置不能为空");
        } else {
            $.post("/cluster_operation/", {
		new_cluster_id:	    new_cluster_id,
		new_cluster_name:   new_cluster_name,
		new_cluster_conf:   new_cluster_conf,
		new_cluster_lable:  new_cluster_lable,
                operation: "cluster_update",
            },
            function(data) {
                alert(data);
            });
            location.href = '/zk_page/';
        };

    });
    //////////////////////
    $("#select_condition").change(function() {
        var $condition = $("#select_condition option:selected").text();
        $("#user_list").empty();
        $.post("/select_user_list/", {
            condition: $condition,
        },
        function(data) {
            for (var i = 0; i < (data.split(",")).length; i++) {
		var check_user = (data.split(","))[i]
		if ( check_user.length != 0){
                $("#user_list").append("<option>" + (data.split(","))[i] + "</option>");
		}
            }

        });
    });
    //////////////////////
    $("#userad_add").click(function() {
	var $new_user = $("#user_text").val();
        var $zk_name = $("#select_condition option:selected").text();
        if ($new_user == "") {
            alert("用户必须增加!!!!!");
        } else {
            $.post("/add_user/", {
		new_user: $.trim($new_user),
		zk_name:  $zk_name,
            },
            function(data) {
                alert(data);

            });
		location.reload(true);
        }

    });
    //////////////////////
    $("#user_delete").click(function() {
        var $zk_name = $("#select_condition option:selected").text();
        var $user = $("#user_list option:selected").text();
        if ($user == "") {
            alert("请先选择要删除的用户!!!!");
        } else {
            $.post("/delete_user/", {
                user: $user,
                zk_name:  $zk_name,
            },
            function(data) {
                alert(data);
        	$("#user_list option:selected").remove();

            });
		location.reload(true);

        }

    });
    //////////////////////
    
    $("#qianyi_btn").click(function() {
	var zk_source = $("#zk_source").val();
	var zk_dest = $("#zk_dest").val();
	var zk_key = $("#zk_qianyikey").val();
	var fdStart = zk_key.indexOf("/");
	if (zk_source.indexOf(":") == -1 || zk_dest.indexOf(":") == -1 ){
	    alert("填写格式:\nip:port")
	}else if (zk_key==""){
	    alert("请填写key");
	}else if (fdStart == -1){
	    alert("必须以/开头");
	
	}else{
            $.post("/begin_qian/", {
                zk_source: zk_source,
                zk_dest: zk_dest,
                zk_key: zk_key,
            },
            function(data) {
                alert(data);

            });
    	}
    });
    //////////////////////
    
    $("#status_zk").click(function() {
	alert("想查看什么,tell me!!!!");
    });
});
