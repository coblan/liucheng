
export class WorkNodeEditor{
    constructor(){
        var self=this
        var url=engine_url+'/'+'workboard.worknode.edit'
        ex.get(url,function(resp){
            self.heads=resp.heads
            self.heads=ex.sort_by_names(self.heads,["short_desp","owner","status","start_time","long_desp"])
            //ex.remove(self.heads,function(head){
            //    if(head.name=="work_group"){
            //        return true
            //    }
            //})

        })


        $(function(){
            $('body').append(`<div id="worknode-editor">
     <modal v-show="show_edit">
        <div @click.stop="" style="max-height: 90vh;max-width: 90vw;">
            <div style="text-align: right;padding-right: 1em;padding-top: 0.3em;">
                <a :href="'/pc/log?rows=workboard.worknode:'+node_kw.row.pk" target="_blank">修改日志</a>
                <button @click="assure_edit()">确定</button>
                <button @click="show_edit=false">取消</button>
            </div>
            <div  class='field-panel'>
                <field  v-for='head in node_kw.heads' :key="head.name" :name='head.name' :kw='node_kw'></field>
            </div>
        </div>

    </modal>
            </div>`)

            self.editor= new Vue({
                el:'#worknode-editor',
                data:{
                    show_edit:false,
                    node_kw:{
                        heads:[],
                        row:{},
                        errors:{},
                    }
                },
                methods:{
                    assure_edit:function(){
                        var self=this
                        show_upload()
                        var post_data=[{fun:'save',row:this.node_kw.row}]
                        ex.post('/_ajax',JSON.stringify(post_data),function(resp){
                            if(resp.save.status=='success'){
                                //var node=ex.findone(self.node_group.nodes,{pk:self.node_kw.row.pk})
                                var node=self.node_kw.row
                                var new_node=resp.save.row
                                ex.assign(node,new_node)
                                hide_upload(300)
                                self.show_edit=false
                                self.callback(node)
                            }

                        })

                    },
                }
            })
        })

    }
    edit(node,callback){
        this.editor.node_kw.heads=this.heads
        this.editor.node_kw.row=ex.copy(node)
        this.editor.show_edit=true
        this.editor.callback=callback
    }
}