import { allTokens } from "./tokens";
import * as fs from 'fs';


// funcion que va a probar el codigo ejemplo

export function lexer(input: string, user: string): void {

    const lines = input.split("\n");
    const log: string[] = []; 

    lines.forEach((line, lineNum) => {

        let text = line.trim();
        while (text.length > 0) {
            let matched = false;
            // ignorar espacios
            const blankS = text.match(/^\s+/);
            if (blankS) {
                text = text.slice(blankS[0].length);
                continue;
            }
            for (const token of allTokens) {
                const match = text.match(token.regex);

                if (match) {
                    log.push(`Reconozco el simbolo '${match[0]}' `);
                    console.log(`Reconozco el simbolo '${match[0]}' `)
                    text = text.slice(match[0].length);
                    matched = true;
                    break;


                }
            }
            

                if (!matched) {
                    log.push(`Error no se reconoce '${text[0]}' `);
                    console.log(`Error no se reconoce '${text[0]}' `);
                    text = text.slice(1);
                }

          


        }
    });

    // Obtener la fecha y hora actuales
    const now = new Date();
    const day = String(now.getDate()).padStart(2, '0'); // Día con dos dígitos
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Mes con dos dígitos (enero es 0)
    const year = now.getFullYear();
    const hours = String(now.getHours()).padStart(2, '0'); // Horas con dos dígitos
    const minutes = String(now.getMinutes()).padStart(2, '0'); // Minutos con dos dígitos

    // Formatear la fecha y hora en el formato deseado
    const dateTimeFormatted = `${day}-${month}-${year}-${hours}h${minutes}`;

    // Escribir el log en un archivo
    const logFileName = `lexico-${user}-${dateTimeFormatted}.txt`;
    fs.writeFileSync(logFileName, log.join('\n'));
    console.log(`Lexer log escrito en ${logFileName}`);

}