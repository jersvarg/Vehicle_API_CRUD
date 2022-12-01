var app= new Vue({
    el: '#app',
    data: {
        message: 'Hi Jerson',
        info:[],
        form:{
            Marca:"",
            Color:"",
            Precio:"",
            Modelo:"",
            Cilindraje:""
        },
        dataEdit:null,
        isEdit:false,
        input_value:"",
    },
    mounted() {
        axios.get("http://127.0.0.1:8000/")
            .then(respuesta=>this.info=respuesta.data)
            .catch(error=>console.log(error));
    },
    methods: {
        onSubmit(){
            if(this.isEdit){                
                axios.put("http://127.0.0.1:8000/"+this.dataEdit._id,this.form)
                .then(res=>{
                    this.isEdit=false;
                    location.reload();
                });
            }
            else{
                axios.post('http://127.0.0.1:8000/',this.form)
                .then(res=>{
                alert("Se agrega un Auto")
                location.reload();
            })
            }            
        },
        onDelete_auto(auto){
            axios.delete('http://127.0.0.1:8000/'+auto._id)
            .then(res=>{                
                location.reload();
            })
            console.log(auto)
        },
        onEdit_auto(auto){
            /*axios.put('http://127.0.0.1:8000/'+auto._id)
            .then(res=>{                
                location.reload();
            })*/
            this.form.Marca=auto.Marca;
            this.form.Color=auto.Color;
            this.form.Precio=auto.Precio;
            this.form.Modelo=auto.Modelo;
            this.form.Cilindraje=auto.Cilindraje;
            this.dataEdit=auto;
            this.isEdit=true
            //console.log(auto) muestra el auto selecionado en consola (html)
        },
        search_car(){
            let item = document.querySelectorAll(".auto_items");
            item.forEach(el=>{
                !el.querySelector(".auto_item_marca").textContent.toLowerCase().includes(this.input_value.toLowerCase())?
                el.classList.add("item_filter"):el.classList.remove("item_filter")
            })
            
        }        
    },    
})