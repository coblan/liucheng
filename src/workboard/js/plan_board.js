
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
        }
    },
    template:`<div class="flex plan">
    <div class="item" v-for="node in row.nodes" @click="edit(node)">
        <div class="center-two" >
            <span v-text="node.short_desp"></span>
        </div>
        <div class="status-icon">
            <span v-if="node.status=='finish'" style="color: #00dd00;"><i class="fa fa-check" aria-hidden="true"></i></span>
            <span v-if="node.start_time"><i class="fa fa-clock-o" aria-hidden="true"></i></span>
        </div>
    </div>
    <div class="item" @click="add_new()">
        <div class="center-two" >
            <i class="fa fa-plus fa-2x" aria-hidden="true"></i>
        </div>
    </div>
    </div>`
}

Vue.component('plan-board',plan_board)