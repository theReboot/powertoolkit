console.log("system.js");

var example1 = new Vue({
  el: '#v-system-table',
  data: {
    agencies: [
      {
        "type": "Agency",
        "name": "NBET",
        "description": "description for NBET goes here and explains what it is and does."
      },
      {
        "type": "Agency",
        "name": "NEMSA",
        "description": "description for NEMSA goes here and explains what it is and does."
      },
      {
        "type": "Agency",
        "name": "REA",
        "description": "description for REA goes here and explains what it is and does."
      },
      {
        "type": "Agency",
        "name": "TCN",
        "description": "description for TCN goes here and explains what it is and does."
      },
      {
        "type": "Agency",
        "name": "NERC",
        "description": "description for NERC goes here and explains what it is and does."
      },
      {
        "type": "Agency",
        "name": "NELMCO",
        "description": "description for NELMCO goes here and explains what it is and does."
      },
      {
        "type": "Agency",
        "name": "NDPHC",
        "description": "description for NDPHC goes here and explains what it is and does."
      }
    ],
    gencos: [
      {
        "type": "Genco",
        "name": "AES",
        "description": "description for AES goes here and explains what it is and does."
      },
      {
        "type": "Genco",
        "name": "Aksa Pow St",
        "description": "description for Aksa goes here and explains what it is and does."
      },
      {
        "type": "Genco",
        "name": "AFam Pow St",
        "description": "description for AFam goes here and explains what it is and does."
      },
      {
        "type": "Genco",
        "name": "Alaoji PS",
        "description": "description for Alaoji goes here and explains what it is and does."
      },
      {
        "type": "Genco",
        "name": "Egbin PS",
        "description": "description for Egbin goes here and explains what it is and does."
      }
    ],
    discos: [
      {
        "type": "Disco",
        "name": "AEDC",
        "description": "description for AEDC goes here and explains what it is and does."
      },
      {
        "type": "Disco",
        "name": "BEDC",
        "description": "description for BEDC goes here and explains what it is and does."
      },
      {
        "type": "Disco",
        "name": "EKEDP",
        "description": "description for EKEDP goes here and explains what it is and does."
      }
    ]
  }
});
