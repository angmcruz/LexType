// Erick Murillo

// Función para verificar si un string es palíndromo
function esPalindromo(s: string): boolean {
    if (s.length <= 1) {
        return true;
    } else {
        if (s[0] === s[s.length - 1]) {
            return esPalindromo(s.substring(1, s.length - 1));
        } else {
            return false;
        }
    }
}

// Función para sumar dígitos de un número
function sumarDigitos(n: number): number {
    if (n === 0) {
        return 0;
    } else {
        return sumarDigitos(Math.floor(n / 10)) + (n % 10);
    }
}

// Pruebas
const palabra1 = "radar";
if (esPalindromo(palabra1)) {
    console.log(`El string "${palabra1}" es un Palíndromo`);
} else {
    console.log(`El string "${palabra1}" no es Palíndromo`);
}

const numero1 = 135;
const numero2 = 67;
const numero3 = 1111;

console.log(`La suma de dígitos de ${numero1} es: ${sumarDigitos(numero1)}`);
console.log(`La suma de dígitos de ${numero2} es: ${sumarDigitos(numero2)}`);
console.log(`La suma de dígitos de ${numero3} es: ${sumarDigitos(numero3)}`);
