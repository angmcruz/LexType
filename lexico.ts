import { allTokens } from "./tokens";


// funcion que va a probar el codigo ejemplo

export function lexer(input: string, user: string): void {

    const lines = input.split("\n");
    const log: string[] = []; 

    lines.forEach((line, lineNum) => {

        let text = line.trim();
        while (text.length > 0) {
            let matched = false;


            for (const token of allTokens) {
                const match = text.match(token.regex);

                if (match) {
                    log.push('No hay errores');
                    text = text.slice(match[0].length);
                    matched = true;
                    break;


                } else {
                    log.push('Simbolo no reconocido')
                    text = text.slice(1);

                }

            }


        }
    });



}