<template>
    <div>
        <nav>
    <md-menu md-direction="bottom-start">
      <md-button md-raised md-primary><a href=""><router-link to="/principal/datos">Mis Datos</router-link></a></md-button>
    </md-menu>

    <md-menu md-direction="bottom-end">
      <md-button md-raised md-primary><router-link to="/principal/formato">Generar Formato</router-link></md-button>
    </md-menu>

    <md-menu md-direction="top-start">
      <md-button md-raised md-primary><router-link to="/principal/bandeja">Bandeja de Entrada</router-link></md-button>

    </md-menu>
    <md-menu md-direction="top-start">
      <md-button md-raised md-primary><router-link to="/principal/bandejasalida">Bandeja de Salida</router-link></md-button>

    </md-menu>
    <md-menu md-direction="top-start" v-if="isAdmin">
      <md-button md-raised md-primary v-if="isAdmin"><router-link to="/principal/adminusers" >Administrar usuarios</router-link></md-button>

    </md-menu>

    <md-menu md-direction="top-end">
      <md-button md-raised md-primary @click="salir()"><a href="">Salir</a></md-button>
    </md-menu>
  </nav>
        <div>
            
            <router-view></router-view>
    </div>
 <md-card md-with-hover v-bind:style="card" >
            <md-ripple>
                <md-card-header>
                    <div class="md-title">Proyecto Criptografía</div>
                    <div class="md-subhead">UPIITA</div>
                </md-card-header>

                <md-card-content>
                   Sistema de Transferencia segura de formatos oficiales empleando firma digital y encriptación.
                   <br> Tecnologías Empleadas:
                   <br> Generación de Llaves y firmado de documentos: RSA / SHA1
                   <br> Cifrado de Archivos: Cifrado simétrico mediante AES, con llave cifrada bajo esquema de llave pública con RSA.
                </md-card-content>

            </md-ripple>
        </md-card>
  </div>
</template>
<script>
import { db } from '../main'
import firebase from 'firebase'
import { functions } from 'firebase';
export default {
    data(){
return{
    show:false,
    isAdmin : localStorage.getItem("isAdmin"),
    nombre:"",
    principal:false,
    usuario : [],
    rfc:localStorage.getItem("rfc"),
    router:this.$router.currentRoute.fullPath,
        card:{
        width:"60%",
        margin:"2em auto auto auto"
    }
}
    },
     methods:{
    
       salir: function() {
      firebase.auth().signOut().then(() => {
                       localStorage.clear();

        this.$router.replace('/login')

      })

    }
  },
  mounted(){
    console.log(this.isAdmin)
      if(this.$router.currentRoute.fullPath=='/principal'){
          this.principal=true
      }
      this.$root.$on('isAdmin', data => {
        console.log(data);
        this.isAdmin = data
    });

  },
  watch:{
  $route (to, from){
        this.principal = false;
        this.router=this.$router.currentRoute.fullPath
    }
      
  }
}
</script>
<style>
nav{
    background-color: #5e2129;

}
a{
    text-decoration: none;
    color: white;
    margin: auto;
    font-size:1em;
    font-weight: bold;
  }

</style>
