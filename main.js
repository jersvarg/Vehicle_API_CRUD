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
        }
    },
    mounted() {
        axios.get("http://127.0.0.1:8000/")
            .then(respuesta=>this.info=respuesta.data)
            .catch(error=>console.log(error));
    },
    methods: {
        onSubmit(){
            axios.post('http://127.0.0.1:8000/',this.form)
            .then(res=>{
                alert("Se agrega un Auto")
                location.reload();
            })
        }
    },
})