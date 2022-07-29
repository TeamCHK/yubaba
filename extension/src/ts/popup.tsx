import React, { useEffect, useState } from "react";
import { createRoot, Root } from "react-dom/client";
import {
    AppBar,
    Card,
    CardContent,
    CardHeader,
    CircularProgress,
    CssBaseline,
    Link,
    Toolbar,
    Typography
} from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import wretch from 'wretch';
import { PopupToBackgroundMsg, BackgroundToPopupMsg, MsgType, MLISResponse } from "./types";

// TODO: Issue #14: Change url and endpoint after MLIS is ready
const apiRoot: string = "http://localhost:8000";
const summarizationEndpoint: string = "/summary";

function Popup () {
    const [isLoading, setIsLoading] = useState(false);
    const [content, setContent] = useState('');
    const [articleTitle, setArticleTitle] = useState('');

    useEffect(() => {
        const msg : PopupToBackgroundMsg = {
            type: MsgType.PopUpInit
        };
        setIsLoading(true);
        chrome.runtime.sendMessage(msg, function(response: BackgroundToPopupMsg) {
            if (response && response.textToSummarize) {
                wretch(apiRoot + summarizationEndpoint)
                .options({mode: "cors"})
                .post({text: response.textToSummarize})
                .json( (mlisResponse: MLISResponse) => {
                    setArticleTitle(response.articleTitle);
                    setContent(mlisResponse.text);
                    setIsLoading(false);
                });
            }
        });
    }, [setContent]);

    return (
        <>
            <CssBaseline />
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" color="common.white" component="div" sx={{ flexGrow: 1 }}>
                        yubaba
                    </Typography>
                    <SettingsIcon />
                </Toolbar>
            </AppBar>
            <Card sx={{ height: 400 }}>
                <CardContent>
                    <Typography sx={{ fontSize: 18 }}>
                        Summary of {articleTitle}: 
                    </Typography>
                </CardContent>
                <CardContent>
                    {(isLoading)
                        ? <CircularProgress /> 
                        : <Typography variant="body2"> {content} </Typography>
                    }
                </CardContent>
            </Card>
        </>
    );
};

export default Popup;
