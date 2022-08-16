import React, { useEffect, useState } from "react";
import {
    AppBar,
    Card,
    CardContent,
    CircularProgress,
    CssBaseline,
    Toolbar,
    Typography
} from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import { MLISRequest, MLISResponse } from "../extension/types";

function Popup() {
    const [isLoading, setIsLoading] = useState(true);
    const [content, setContent] = useState('');
    const [articleTitle, setArticleTitle] = useState('');

    useEffect(() => {
        const request: MLISRequest = {
            url: window.location.href,
        };
        chrome.runtime.sendMessage(request, (response: MLISResponse) => {
            if (response && response.articleSummary) {
                setArticleTitle(response.articleTitle);
                setContent(response.articleSummary);
                setIsLoading(false);
            }
        });
    }, []);

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
