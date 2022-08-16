export type MLISRequest = {
    url: string,
}

export type MLISResponse = {
    articleSummary: string,
    articleTitle?: string,
    articleAuthors?: string[],
    publishDate?: Date,
};
