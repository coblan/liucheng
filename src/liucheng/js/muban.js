
export class MubanManager{
    constructor(muban_table_url){
        this.table_url=muban_table_url
        this.vue_inst=null
        this.select_callback=null
    }
    select(callback){
        if(!this.vue_inst){
            this.vue_inst=this._mount()
        }
        this.vue_inst.show_me=true
        this.select_callback=callback
    }
    _mount(){
        $('body').append(`<div id="_muban_list">
        <modal v-show="show_me" @click.native="show_me=false">
              <muban-list class="muban-list" @click.native.stop="" table_url="${this.table_url}"></muban-list>
        </modal>
        </div>`)
        var manager=this
        window._muban_list=new Vue({
            el:'#_muban_list',
            data:{
                show_me:false
            },
            mounted:function(){
                this.$on('row-click',function(row){
                    manager.select_callback(row)
                })
            }
        })
        return  window._muban_list
    }
}

function emit_to_parent(com_inst,event_name,arg){
    var par=com_inst.$parent
    while(par){
        var rt = par.$emit(event_name,arg)
        par=par.$parent
    }
}

var muban_list={
    props:['table_url'],
    data:function(){
        return {
            heads:[],
            rows:[],
            row_pages:{
                options:[],
                crt_page:1,
            }
        }
    },
    mixins:[table_fun],
    mounted:function(){
        this.goto_page(1)
    },
    methods:{
        goto_page:function(page_num){
            var self=this
            var url=ex.appendSearch(this.table_url,{_page:page_num})
            ex.get(url,function(resp){

                self.heads=resp.heads
                self.rows=resp.rows
                self.row_pages=resp.row_pages

                self.heads[0].type="click-td"
                ex.each(self.heads,function(head){
                    if(head.name=='relations'){
                        head.type="flowchart-td"
                    }
                })

            })
        }
    },
    template:`<div>
        <com-table class='table fake-suit' :has_check="false" :map="map"
            :heads="heads" :rows="rows" v-model="selected"></com-table>

        <paginator :nums='row_pages.options' :crt='row_pages.crt_page' @goto_page='goto_page($event)'></paginator>
    </div>`,
}
Vue.component('muban-list',muban_list)

var click_td={
    props:['name','row'],
    template:`<span style="cursor: pointer;"  @click="on_click()" v-text="row[name]"></span>`,
    methods:{
        on_click:function(){
            //this.$parent.$emit('row-click',this.row)
            emit_to_parent(this,'row-click',this.row)
        }
    }
}
Vue.component('click-td',click_td)