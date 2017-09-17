
require('./scss/plan_board.scss')
import {WorkNodeEditor} from  './worknode.js'

var node_editor=new WorkNodeEditor()

var plan_board={
    props:['row','name'],
    methods:{
      add_new:function(){
          var init_node={

          }
          node_editor.edit( init_node,function(node){


          })
      }
    },
    template:`<div class="flex plan">
    <div class="item">
        <div class="center-two">hello world</div>
    </div>
    <div class="item">
        <div class="center-two" @click="add_new()">
            <i class="fa fa-plus fa-2x" aria-hidden="true"></i>
        </div>
    </div>
    </div>`
}

Vue.component('plan-board',plan_board)