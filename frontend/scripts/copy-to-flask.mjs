import { cp, rm } from 'node:fs/promises'
import { resolve } from 'node:path'

const source = resolve('dist')
const destination = resolve('../backend/frontend_dist')
await rm(destination, { recursive: true, force: true })
await cp(source, destination, { recursive: true })
console.log(`Copied production frontend to ${destination}`)
