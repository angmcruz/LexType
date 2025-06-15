import { allTokens } from "./tokens";


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



}