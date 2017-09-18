
require('./scss/plan_board.scss')
import {WorkNodeEditor} from  './worknode.js'

var node_editor=new WorkNodeEditor()

var plan_board={
    props:['row','name'],
    //computed:{
    //  nodes:function(){
    //      return this.row.nodes
    //  }
    //},
    data:function(){
        return {
            gb:gb,
        }
    },

    methods:{
      add_new:function(){
          var self=this
          var init_node={
              work_group:self.row.pk,
              status:'waiting',
              start_time:'',
              _class:'workboard.worknode'
          }
          node_editor.edit( init_node,function(node){
                self.row.nodes.push(node)
          })
      },
        edit:function(node){
            var tmp_node=ex.copy(node)
            node_editor.edit( tmp_node,function(rt_node){
                ex.assign(node,rt_node)
            })
        },
        delete_node:function(node){
            var r = confirm('真的删除吗？')
            if(r){
                ex.remove(this.row.nodes,node)
                var post_data=[{fun:'del_rows',rows:[node]}]
                ex.post('/_ajax',JSON.stringify(post_data),function(resp){

                })
            }
        },
        is_match_search:function(node){
            return is_matched_node(node)
        }
    },
    template:`<div class="flex plan">
    <div :class="['item',{'matched':is_match_search(node)}]" v-for="node in row.nodes" @click="edit(node)">
        <div class="center-two text" >
            <span v-text="node.short_desp"></span>
        </div>
        <div class="status-icon">
            <span v-if="node.status=='finish'" style="color: #00dd00;"><i class="fa fa-check" aria-hidden="true"></i></span>
            <span v-if="node.start_time"><i class="fa fa-clock-o" aria-hidden="true"></i></span>
        </div>
        <div class="delete-icon" v-if="gb.node_edit_state" @click.stop="delete_node(node)">
            <span><i class="fa fa-trash" aria-hidden="true"></i></span>
        </div>
    </div>
    <div class="item" @click="add_new()" v-if="gb.node_edit_state">
        <div class="center-two" >
            <i class="fa fa-plus fa-2x" aria-hidden="true"></i>
        </div>
    </div>
    </div>`
}

Vue.component('plan-board',plan_board)


function is_matched_node(node){
    if(!node.start_time){
        return false
    }
    if (search_args.owner){
        if(node.owner!=search_args.owner){
            return false
        }
    }
    if(search_args._start_start_time){
        if(node.start_time< search_args._start_start_time) {
            return false
        }
    }
    if(search_args._end_start_time){
        if(node.start_time > search_args._end_start_time){
            return false
        }
    }
    if(search_args.node_status){
        if(node.status!=search_args.node_status){
            return false
        }
    }
    if(!search_args._start_start_time && !search_args._end_start_time && !search_args.node_status && !search_args.owner){
        return false
    }
    return true

}