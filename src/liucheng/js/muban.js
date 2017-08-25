
export class MubanManager{
    constructor(muban_table_url){
        this.table_url=muban_table_url
        this.vue_inst=null
    }
    select(){
        if(!this.vue_inst){
            this.vue_inst=this._mount()
        }
        this.vue_inst.show_me=true
    }
    _mount(){
        $('body').append(`<div id="_muban_list">
        <modal v-show="show_me" @click.native="show_me=false">
              <muban-list @click.native.stop="" table_url="${this.table_url}"></muban-list>
        </modal>
        </div>`)

        window._muban_list=new Vue({
            el:'#_muban_list',
            data:{
                show_me:false
            }
        })
        return  window._muban_list
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

            })
        }
    },
    template:`<div>
        <com-table class='table fake-suit' :has_check="false"
            :heads="heads" :rows="rows" v-model="selected"></com-table>

        <paginator :nums='row_pages.options' :crt='row_pages.crt_page' @goto_page='goto_page($event)'></paginator>
    </div>`,
}
Vue.component('muban-list',muban_list)


