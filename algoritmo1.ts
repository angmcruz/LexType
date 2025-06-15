/*Javier Murillo*/

// Contar cuántos números pares hay en un array
function contarPares(numeros: number[]): number {
 let contador = 0;
 for (let i = 0; i < numeros.length; i++) {
 if (numeros[i] % 2 === 0) {
 contador++;
 }
 }
 return contador;
}
let arreglo: number[] = [2, 5, 8, 9, 12, 15];
console.log(`Cantidad de números pares: ${contarPares(arreglo)}`);

// Verificar si todos los valores de un Map son mayores a cierto valor
function todosMayoresA(m: Map<string, number>, umbral: number): boolean {
 for (let valor of m.values()) {
 if (valor <= umbral) {
 return false;
 }
 }
 return true;
}
let salarios: Map<string, number> = new Map([
 ["Luis", 500],
 ["Ana", 800],
 ["Carlos", 1200]
]);
const umbral = 400;
if (todosMayoresA(salarios, umbral)) {
 console.log("Todos los salarios son mayores al umbral.");
} else {
 console.log("Hay salarios menores o iguales al umbral.");
}

/*Javier Murillo*/