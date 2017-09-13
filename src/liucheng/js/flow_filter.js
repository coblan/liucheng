export  function flow_has_node_delay(flow){
    /*
    查询流程图是否有延期的节点
    *
    * */
    var today=get_today_str()
    for(var i=0;i<flow.nodes.length;i++){
        var node=flow.nodes[i]
        if(node.status=='waiting' && node.start_time && node.start_time< today){
            return true
        }
    }
    return false
}

function get_today_str(){
    var now=new Date()
    var year=now.getFullYear()
    var month=now.getMonth()+1
    if (month<10){month='0'+month}
    var day=now.getDate()
    if(day<10){day='0'+day}

    return `${year}-${month}-${day}`
}

