FROM node:24-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN corepack enable pnpm && pnpm install

COPY . .
 
RUN pnpm build
 
EXPOSE 3000                                                                                                                                                                                                                                                                                                                                                            

ENV PORT=3000                                                                                                                                                                                                                                                                                                                                                          

CMD ["pnpm", "start"]    
