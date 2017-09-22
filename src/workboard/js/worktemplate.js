
require('./scss/worktemplate.scss')

export class WorkTemplateEditor{
    constructor(){
        var self=this

        $(function(){
            $('body').append(`<div id="worktemplate-editor">
     <modal v-show="show_edit">
        <div @click.stop="" style="max-height: 90vh;max-width: 90vw;min-height: 40em;min-width: 50em;">
            <div style="text-align: right;padding-right: 1em;padding-top: 0.3em;">
                <!--<a :href="'/pc/log?rows=workboard.worknode:'+node_kw.row.pk" target="_blank">修改日志</a>-->
                <button @click="assure_edit()">确定</button>
                <button @click="show_edit=false">取消</button>
            </div>
            <div  class='field-panel'>
                <field  v-for='head in kw.heads' :key="head.name" :name='head.name' :kw='kw'></field>
            </div>
        </div>

    </modal>
            </div>`)

            self.editor= new Vue({
                el:'#worktemplate-editor',
                data:{
                    show_edit:false,
                    editable:true,
                    kw:{
                        heads:[{name:'short_desp',type:'linetext',label:'简短描述'},{name:'long_desp',type:'blocktext',label:'详细描述'}],
                        row:{short_desp:'',long_desp:''},
                        errors:{},
                    }
                },
                methods:{
                    assure_edit:function(){
                        this.callback(this.kw.row)
                        this.show_edit=false
                    },

                }
            })
        })

    }
    edit(node,callback){
        //this.editor.node_kw.heads=this.heads
        this.editor.kw.row=ex.copy(node)
        this.editor.show_edit=true
        this.editor.callback=callback
    }
    set_editable(editable){
    if(editable){
        this.editor.kw.heads=[{name:'short_desp',type:'linetext',label:'简短描述'},{name:'long_desp',type:'blocktext',label:'详细描述'}]
    }else{
        this.editor.kw.heads=[{name:'short_desp',type:'linetext',label:'简短描述',readonly:true},{name:'long_desp',type:'blocktext',label:'详细描述',readonly:true}]
    }
}
}

var editor= new WorkTemplateEditor()

var com_worktemplate_pan={
    props:['content','editable'],
    //data:function(){
    //
    //    return {
    //
    //    }
    //},
    template:`<div class="flex work-template-pan">
        <div class="item" v-for="node in content" @click="edit(node)">
            <div class="center-two" >
                <span v-text="node.short_desp"></span>
            </div>

        </div>
        <div v-if="editable" class="item" @click="add_new()">
            <div class="center-two">
                <i class="fa fa-plus fa-2x" aria-hidden="true"></i>
            </div>
        </div>
    </div>`,
    methods:{
        add_new:function(){
            var new_content={
                short_desp:'工作步骤',
                long_desp:''
            }
            this.content.push(new_content)
        },
        edit:function(node){
            editor.set_editable(this.editable)
            editor.edit(node,function(new_node){
                ex.assign(node,new_node)
            })
        }
    }

}

Vue.component('com-worktemplate-pan',com_worktemplate_pan)