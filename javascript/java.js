"use strict";

function delay(ms){return new Promise(resolve => setTimeout(resolve, ms))}

async function fire(){ 
        await delay(100);
        console.log("teste")
    }
document.addEventListener("DOMContentLoaded", async function() {await fire()})