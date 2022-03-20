import values from "./BrockInfo";
import val from "./CanadaInfo";
/**
 * @callback BrockInfo
 * @callback CanadaInfo
 * @param {the name of the text wanted} name 
 * @returns the appropriate text from CanadaInfo or BrockInfo
 */
function process(name){
    var url = window.location.href.toString();
    var isCanada = url.search("/canada");
    return isCanada===-1?values[document.documentElement.lang][name]:val[document.documentElement.lang][name];
}

export default process;