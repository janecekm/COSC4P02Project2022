import values from "./BrockInfo";
import val from "./CanadaInfo";
function process(name){
    var temp = window.location.href.toString();
    var v = temp.search("/canada");
    return v==-1?values[document.documentElement.lang][name]:val[document.documentElement.lang][name];
}

export default process;