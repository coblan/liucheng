
require('./scss/flowchart.scss')

var flowchart_base={
    template:`<div class="mermaid" v-text="memraid_text">
    </div>`,
    props:['node_group'],
    mounted:function(){

    },
    computed:{
        memraid_text:function(){
            var text="graph LR;"
            ex.each(this.node_group.nodes,function(node){
                if(node.short_desp){
                    text+=ex.template('{id}["{desp}"];',{id:node.id,desp:node.short_desp})
                }else{
                    text+=ex.template('{id};',{id:node.id})
                }
            })
            ex.each(this.node_group.relations,function(relation){
                text+= ex.template("{src}-->{dst};",{src:relation[0],dst:relation[1]})
            })
            ex.each(this.node_group.nodes,function(node){
                text+=`class ${node.pk} ${node.status};`
            })
            return text
        }
    }
}
Vue.component('com-flowchart',flowchart_base)

var flowchart_td={
    props:['name','row',],
    template:` <div class="mermaid" v-text="memraid_text"></div>`,
    mounted:function(){
        this.render()
    },
    watch:{
        memraid_text:function () {
            this.render()
        }
    },
    computed:{
        node_group:function(){
            var node_group_local=ex.copy(this.row)
            //node_group_local.relations=JSON.parse(node_group_local.relations)
            return node_group_local
        },
        memraid_text:function(){
            var text="graph LR;"
            ex.each(this.node_group.nodes,function(node){
                if(node.short_desp){
                    text+=ex.template('{id}["{desp}"];',{id:node.id,desp:node.short_desp})
                }else{
                    text+=ex.template('{id};',{id:node.id})
                }
            })
            ex.each(this.node_group.relations,function(relation){
                text+= ex.template("{src}-->{dst};",{src:relation[0],dst:relation[1]})
            })

            ex.each(this.node_group.nodes,function(node){
                text+=`class ${node.pk} ${node.status};`
            })
            return text
        }
    },
    methods:{
        render:function(){
            var self=this
            $(this.$el).attr('data-processed','')
            Vue.nextTick(function(){
                mermaid.init({noteMargin: 10}, self.$el);

                //setTimeout(function(){
                //    svgPanZoom( $(self.$el).find('svg')[0])
                //})
                setTimeout(function(){
                    ex.each(self.node_group.nodes,function(node){
                        if(node.owner){
                            mount_user_image(node.pk,node._owner_label,node.head_img)
                        }
                    })
                })
            })
        },
    }

}
Vue.component('flowchart-td',flowchart_td)


var mb_flowchart_base={
    template:`<div class="mermaid" v-text="memraid_text" style="text-align: center">
    </div>`,
    props:['node_group'],
    mounted:function(){
        this.render()
    },
    watch:{
        memraid_text:function () {
            this.render()
        },
    },
    computed:{
        memraid_text:function(){
            var text="graph TB;"
            ex.each(this.node_group.nodes,function(node){
                if(node.short_desp){
                    text+=ex.template('{id}["{desp}"];',{id:node.id,desp:node.short_desp})
                }else{
                    text+=ex.template('{id};',{id:node.id})
                }
            })
            ex.each(this.node_group.relations,function(relation){
                text+= ex.template("{src}-->{dst};",{src:relation[0],dst:relation[1]})
            })
            ex.each(this.node_group.nodes,function(node){
                text+=`class ${node.pk} ${node.status};`
            })
            return text
        }
    },
    methods:{
        render:function(){
            var self=this
            $(this.$el).attr('data-processed','')
            Vue.nextTick(function(){
                mermaid.init({noteMargin: 10}, self.$el);
            })
        },
    }
}
Vue.component('com-flowchart_mb',mb_flowchart_base)

export function mount_user_image(myid,name,head) {
    var head=head || '/static/image/user.jpg'
    var svgimg = document.createElementNS('http://www.w3.org/2000/svg','image');
    svgimg.setAttributeNS('http://www.w3.org/1999/xlink','href', head);
    svgimg.setAttributeNS(null,'height','30');
    svgimg.setAttributeNS(null,'width','30');
    svgimg.setAttributeNS(null,'x','0');
    svgimg.setAttributeNS(null,'y','20');
    svgimg.setAttributeNS(null, 'visibility', 'visible');
    svgimg.innerHTML=`<title>${name}</title>`;
    document.getElementById(myid).appendChild(svgimg);
}
