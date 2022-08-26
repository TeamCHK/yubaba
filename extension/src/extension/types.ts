export type MLISRequest = {
    url: string,
}

export type MLISResponse = {
    status: number,
    message?: string,
    articleSummary?: string,
    articleTitle?: string,
    articleAuthors?: string[],
    publishDate?: Date,
}
