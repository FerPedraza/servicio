<template>
  <div>
    <a11y-dialog id="app-dialog" app-root="#app" @dialog-ref="assignDialogRef">
      <div v-bind:style="modal">
        <h1 v-bind:style="modal" slot="title">Mensaje enviado con exito :)</h1>
        <div>
          <p v-bind:style="modal">{{mensaje_verificacion}}</p>
        </div>
      </div>
    </a11y-dialog>
    <md-card v-bind:style="card" style="border-radius=2em">
      <md-card-header>
        <div class="md-title">Administración de usuarios del sistema</div>
      </md-card-header>

      <md-card-content>
        <label>Usuarios registrados en la base de datos</label>
        <md-card-actions>
          <md-button v-bind:style="color" @click="showModal = true">Agregar Usuario</md-button>
        </md-card-actions>
        <div v-if="showModal">
          <transition name="modal">
            <div class="modal-mask">
              <div class="modal-wrapper">
                <div class="modal-container">
                  <md-card-content>
                    <label class="md-title">Ingrese los datos del nuevo usuario</label>
                    <md-list>
                      <md-list-item>
                        <md-field>
                          <label>Nombre</label>
                          <md-input v-model="nombre"></md-input>
                        </md-field>
                      </md-list-item>
                      <md-list-item>
                        <md-field>
                          <label>Email</label>
                          <md-input v-model="email"></md-input>
                        </md-field>
                      </md-list-item>
                      <md-list-item>
                        <md-field>
                          <label>Estatus inicial</label>
                          <md-input v-model="status"></md-input>
                        </md-field>
                      </md-list-item>
                      <md-list-item>
                        <md-field>
                          <label>RFC</label>
                          <md-input v-model="RFC"></md-input>
                        </md-field>
                      </md-list-item>
                      <md-list-item>
                        <md-field>
                          <label>Cargo</label>
                          <md-input v-model="cargo"></md-input>
                        </md-field>
                      </md-list-item>
                      <md-list-item>
                        <md-field>
                          <label>Departamento</label>
                          <md-input v-model="departamento"></md-input>
                        </md-field>
                      </md-list-item>
                    </md-list>

                    <md-button v-bind:style="color" @click="showModal = false">Cancelar</md-button>
                    <md-button v-bind:style="color" @click="agregarUsuarios()">Aceptar</md-button>
                  </md-card-content>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <md-list>
          <md-list-item v-for="destinatario in destinatarios" >
            <label class="md-list-item-text">{{destinatario.nombre}}</label>
            <md-content class="md-primary">{{destinatario.estado}}</md-content>
            
            <md-menu
              md-direction="bottom-start"
              md-size="medium"
              :md-offset-x="127"
              :md-offset-y="-36"
            >
              <md-button md-menu-trigger>
                <md-icon>menu</md-icon>
              </md-button>

              <md-menu-content>
                <md-menu-item @click="eliminarUsuario(destinatario.nombre)">Eliminar</md-menu-item>
                <md-menu-item @click="inhabilitarUsuario(destinatario.nombre)">Inhabilitar</md-menu-item>
                <md-menu-item @click="activarUsuario(destinatario.nombre)">Activar</md-menu-item>
              </md-menu-content>
            </md-menu>
          </md-list-item>
        </md-list>
      </md-card-content>
    </md-card>
  </div>
</template>
<script>
import pdf from "@/Plantilla";
import { db } from "../main";
import { functions } from "firebase";
import jsPDF from "jspdf";

var RSA = require("jsrsasign");
var d = new Date();
var fecha = d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear();
export default {
  data() {
    return {
      showModal: false,
      rfc: localStorage.getItem("rfc"),
      remitente: localStorage.getItem("nombre"),
      public_remitente: localStorage.getItem("public_key"),
      private_remitente: localStorage.getItem("private_key"),
      cifrar: true,
      color: {
        background: "#5e2129",
        color: "white"
      },
      opcion: {
        zindex: "-1",
        background: "white"
      },
      card: {
        width: "50%",
        height: "100%",
        margin: "3em auto auto auto"
      },
      modal: {
        color: "#5e2129",
        fontweight: "bold"
      },
      menu: [
        { title: "Eliminar" },
        { title: "Inhabilitar" },
        { title: "Activar" }
      ],
      cuerpoTexto: "",
      destinatario_rfc: "",
      destinatario_public: "",
      destinatario: "",
      contenido_cifrado: "",
      llave_cifrado: "",
      destinatarios: [],
      mensaje_verificacion: "",
      nombre: "",
      email: "",
      status: "",
      RFC: "",
      cargo: "",
      departamento: ""

    };
  },
  firestore() {
    db.collection("usuarios")
      .get()
      .then(snap => {
        snap.forEach(doc => {
          this.destinatarios.push({
            nombre: doc.data().nombre,
            estado: doc.data().estado
          });
        });
      });
  },

  methods: {
    assignDialogRef(dialog) {
      this.dialog = dialog;
    },
    agregarUsuario: function(RFC) {
      let llaves = RSA.KEYUTIL.generateKeypair("RSA", 512);
      db.collection("usuarios")
        .doc(RFC)
        .update({
          private_key: RSA.KEYUTIL.getPEM(llaves.prvKeyObj, "PKCS8PRV"),
          public_key: RSA.KEYUTIL.getPEM(llaves.pubKeyObj)
        });
    },
    agregarUsuarios: function() {
      let data = {
        cargo: this.cargo,
        departamento: this.departamento,
        email: this.email,
        estado: this.status,
        nombre: this.nombre,
        private_key: "",
        public_key: "",
        rfc: this.RFC
        };
      db.collection('usuarios').doc(this.RFC);
      db.collection('usuarios').doc(this.RFC).set(data);
      this.agregarUsuario(this.RFC)
      console.log("Fertig!");
      this.showModal = false
    },
    eliminarUsuario: function(name) {
      db.collection("usuarios")
        .where("nombre", "==", name)
        .get()
        .then(snap => {
          return snap.docs[0].ref.delete();
        })
        .then(() => {
          console.log("Successfully updated the record");
        })
        .catch(error => {
          console.error("There was an error editing the record: " + error);
        });
    },
    inhabilitarUsuario: function(name) {
      db.collection("usuarios")
        .where("nombre", "==", name)
        .get()
        .then(snap => {
          return snap.docs[0].ref.update({
            estado: "Inhabilitado"
          });
        })
        .then(() => {
          console.log("Successfully updated the record");
        })
        .catch(error => {
          console.error("There was an error editing the record: " + error);
        });
    },
    activarUsuario: function(name) {
      db.collection("usuarios")
        .where("nombre", "==", name)
        .get()
        .then(snap => {
          return snap.docs[0].ref.update({
            estado: "Activo"
          });
        })
        .then(() => {
          console.log("Successfully updated the record");
        })
        .catch(error => {
          console.error("There was an error editing the record: " + error);
        });
    }
  },
  watch: {
    destinatario: function() {
      db.collection("usuarios")
        .where("nombre", "==", this.destinatario)
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.destinatario_rfc = doc.data().rfc;
            this.destinatario_public = doc.data().public_key;
          });
        });
    }
  }
};
</script>
<style>
.md-radio {
  display: flex;
}

@keyframes click-wave {
  0% {
    height: 40px;
    width: 40px;
    opacity: 0.35;
    position: relative;
  }

  100% {
    height: 200px;
    width: 200px;
    margin-left: -80px;
    margin-top: -80px;
    opacity: 0;
  }
}

.option-input {
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  -o-appearance: none;
  appearance: none;
  position: relative;
  top: 13.33333px;
  right: 0;
  bottom: 0;
  left: 0;
  height: 40px;
  width: 40px;
  transition: all 0.15s ease-out 0s;
  background: #cbd1d8;
  border: none;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  margin-right: 0.5rem;
  outline: none;
  position: relative;
  z-index: 1000;
}

.option-input:hover {
  background: #9faab7;
}

.option-input:checked {
  background: #5e2129;
}

.option-input:checked::before {
  height: 40px;
  width: 40px;
  position: absolute;
  content: "✔";
  display: inline-block;
  font-size: 26.66667px;
  text-align: center;
  line-height: 40px;
}

.option-input:checked::after {
  -webkit-animation: click-wave 0.65s;
  -moz-animation: click-wave 0.65s;
  animation: click-wave 0.65s;
  background: #40e0d0;
  content: "";
  display: block;
  position: relative;
  z-index: 100;
}

.option-input.radio {
  border-radius: 50%;
}

.option-input.radio::after {
  border-radius: 50%;
}
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 700px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>