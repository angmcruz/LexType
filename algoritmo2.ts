
/* Melissa Cruz */ 
//Algoritmo para verificar si un map y un set tienen los mismos elementos
let frutasSet: Set<string> = new Set(["manzana", "pera", "uva"]);
let frutasMap: Map<string, number> = new Map([
 ["manzana", 1],
 ["pera", 2],
 ["uva", 3],
]);
function tienenMismosElementos(set: Set<string>, map: Map<string, number>): boolean {
 if (set.size !== map.size) return false;
 for (let item of set) {
 if (!map.has(item)) return false;
 }
 return true;
}
if (tienenMismosElementos(frutasSet, frutasMap)) {
 console.log("El Set y el Map tienen los mismos elementos.");
} else {
 console.log("El Set y el Map son diferentes.");
}
 

