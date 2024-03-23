"""
make it possible to set default account and save it as a variable??

Where you left off. make get_accounts work

"""

    #############
    # Brokerage #
    #############

    def get_accounts(self, user_id: str) -> Response | Awaitable[Response]:
        """Grabs all the accounts associated with the User.

        Arguments:
        ----
        user_id (str): The Username of the account holder.

        Returns:
        ----
        (dict): All the user accounts.
        """
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint(url="users/{username}/accounts".format(username=user_id))

        # define the arguments
        params = {"access_token": self._access_token}

        return self._get_request(url=url_endpoint, params=params)

    def get_wallets(self, account_id: str) -> Response | Awaitable[Response]:
        """Grabs a A valid crypto Account ID for the authenticated user.

        Arguments:
        ----
        user_id (str): The Username of the account holder.

        Returns:
        ----
        (dict): All the user accounts.
        """
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint(url=f"brokerage/accounts/{account_id}/wallets")

        # define the arguments
        params = {"access_token": self._access_token}

        return self._get_request(url=url_endpoint, params=params)

    def get_balances(self, account_keys: list[str | int]) -> Response | Awaitable[Response]:
        """Grabs all the balances for each account provided.

        Args:
        ----
        account_keys (List[str]): A list of account numbers. Can only be a max
            of 25 account numbers

        Raises:
        ----
        ValueError: If the list is more than 25 account numbers will raise an error.

        Returns:
        ----
        dict: A list of account balances for each of the accounts.
        """
        # validate the token.
        self._token_validation()

        # argument validation.
        account_keys_str = ""
        if not account_keys or not isinstance(account_keys, list):
            raise ValueError("You must pass a list with at least one account for account keys.")
        elif len(account_keys) > 0 and len(account_keys) <= 25:
            account_keys_str = ",".join(map(str, account_keys))
        elif len(account_keys) > 25:
            raise ValueError("You cannot pass through more than 25 account keys.")

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"brokerage/accounts/{account_keys_str}/balances")

        # define the arguments
        params = {"access_token": self._access_token}

        return self._get_request(url=url_endpoint, params=params)

    def get_balances_bod(self, account_keys: list[str | int]) -> Response | Awaitable[Response]:
        """Grabs the beginning of day balances for each account provided.

        Args:
        ----
        account_keys (List[str]): A list of account numbers. Can only be a max
            of 25 account numbers

        Raises:
        ----
        ValueError: If the list is more than 25 account numbers will raise an error.

        Returns:
        ----
        dict: A list of account balances for each of the accounts.
        """
        # validate the token.
        self._token_validation()

        # argument validation.
        account_keys_str = ""
        if not account_keys or not isinstance(account_keys, list):
            raise ValueError("You must pass a list with at least one account for account keys.")
        elif len(account_keys) > 0 and len(account_keys) <= 25:
            account_keys_str = ",".join(map(str, account_keys))
        elif len(account_keys) > 25:
            raise ValueError("You cannot pass through more than 25 account keys.")

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"brokerage/accounts/{account_keys_str}/bodbalances")

        # define the arguments
        params = {"access_token": self._access_token}

        return self._get_request(url=url_endpoint, params=params)

    def get_positions(
        self, account_keys: list[str | int], symbols: Optional[list[str]] = None
    ) -> Response | Awaitable[Response]:
        """Grabs all the account positions.

        Arguments:
        ----
        account_keys (List[str]): A list of account numbers..

        symbols (List[str]): A list of ticker symbols, you want to return.

        Raises:
        ----
        ValueError: If the list is more than 25 account numbers will raise an error.

        Returns:
        ----
        dict: A list of account balances for each of the accounts.
        """
        # validate the token.
        self._token_validation()

        # argument validation, account keys.
        account_keys_str = ""
        if not account_keys or not isinstance(account_keys, list):
            raise ValueError("You must pass a list with at least one account for account keys.")
        elif len(account_keys) > 0 and len(account_keys) <= 25:
            account_keys_str = ",".join(map(str, account_keys))
        elif len(account_keys) > 25:
            raise ValueError("You cannot pass through more than 25 account keys.")

        # argument validation, symbols.
        if symbols is None:
            params = {"access_token": self._access_token}

        elif not symbols:
            raise ValueError("You cannot pass through an empty symbols list for the filter.")
        else:
            symbols_formatted = [f"Symbol eq {symbol!r}" for symbol in symbols]
            symbols_str = "or ".join(symbols_formatted)
            params = {"access_token": self._access_token, "$filter": symbols_str}

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"brokerage/accounts/{account_keys_str}/positions")

        return self._get_request(url=url_endpoint, params=params)

    def get_orders(
        self, account_keys: list[str | int], page_size: int = 600, order_ids: Optional[list[str | int]] = None
    ) -> Response | Awaitable[Response]:
        """Grab all the account orders for a list of accounts.

        Overview:
        ----
        This endpoint is used to grab all the order from a list of accounts provided. Additionally,
        each account will only go back 14 days when searching for orders.

        Arguments:
        ----
        account_keys (List[str]): A list of account numbers.

        since (int): Number of days to look back, max is 14 days.

        page_size (int): The page size.

        page_number (int, optional): The page number to return if more than one. Defaults to 0.

        Raises:
        ----
        ValueError: If the list is more than 25 account numbers will raise an error.

        Returns:
        ----
        dict: A list of account balances for each of the accounts.
        """
        # validate the token.
        self._token_validation()

        # argument validation, account keys.
        account_keys_str = ""
        if not account_keys or not isinstance(account_keys, list):
            raise ValueError("You must pass a list with at least one account for account keys.")
        elif len(account_keys) > 0 and len(account_keys) <= 25:
            account_keys_str = ",".join(map(str, account_keys))
        elif len(account_keys) > 25:
            raise ValueError("You cannot pass through more than 25 account keys.")

        # Argument Validation, Order IDs
        if order_ids and len(order_ids) > 0 and len(order_ids) <= 50:
            order_ids_str = f'/{",".join(map(str, order_ids))}'
        elif order_ids and len(order_ids) > 50:
            raise ValueError("You cannot pass through more than 50 Orders.")
        else:
            order_ids_str = ""

        if 600 < page_size < 0 or not isinstance(page_size, int):
            raise ValueError("Page Size must be an integer, [1..600]")

        params = {
            "access_token": self._access_token,
            "pageSize": page_size,
        }

        # define the endpoint.
        url_endpoint = self._api_endpoint(url=f"brokerage/accounts/{account_keys_str}/orders{order_ids_str}")

        return self._get_request(url=url_endpoint, params=params)

    def get_historical_orders(
        self,
        account_keys: list[str | int],
        since: date,
        page_size: int = 600,
        order_ids: Optional[list[str | int]] = None,
    ) -> Response | Awaitable[Response]:
        """Grab all the account orders for a list of accounts.

        Overview:
        ----
        This endpoint is used to grab all the order from a list of accounts provided. Additionally,
        each account will only go back 14 days when searching for orders.

        Arguments:
        ----
        account_keys (List[str]): A list of account numbers.

        since (int): Number of days to look back, max is 14 days.

        page_size (int): The page size.

        page_number (int, optional): The page number to return if more than one. Defaults to 0.

        Raises:
        ----
        ValueError: If the list is more than 25 account numbers will raise an error.

        Returns:
        ----
        dict: A list of account balances for each of the accounts.
        """
        # Argument validation, account keys.
        if not since:
            since = date.today() - timedelta(days=90)

        if 600 < page_size < 0 or not isinstance(page_size, int):
            raise ValueError("Page Size must be an integer, [1..600]")

        account_keys_str = ""
        if not account_keys or not isinstance(account_keys, list):
            raise ValueError("You must pass a list with at least one account for account keys.")
        elif len(account_keys) > 0 and len(account_keys) <= 25:
            account_keys_str = ",".join(map(str, account_keys))
        elif len(account_keys) > 25:
            raise ValueError("You cannot pass through more than 25 account keys.")

        # Argument Validation, Order IDs
        if order_ids and len(order_ids) > 0 and len(order_ids) <= 50:
            order_ids_str = f'/{",".join(map(str, order_ids))}'
        elif order_ids and len(order_ids) > 50:
            raise ValueError("You cannot pass through more than 50 Orders.")
        else:
            order_ids_str = ""

        # Argument Validation, Since
        if since < date.today() - timedelta(days=90):
            raise ValueError("Limited to 90 days prior to the current date.")

        # validate the token.
        self._token_validation()

        params = {
            "access_token": self._access_token,
            "since": since,
            "pageSize": page_size,
        }

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"brokerage/accounts/{account_keys_str}/historicalorders{order_ids_str}")

        return self._get_request(url=url_endpoint, params=params)

    ###############
    # Market Data #
    ###############

    def get_bars(
        self,
        symbol: str,
        interval: int,
        unit: str,
        barsback: int,
        firstdate: datetime,
        lastdate: datetime,
        sessiontemplate: str,
    ) -> Response | Awaitable[Response]:
        """Grabs all the accounts associated with the User.

        Arguments:
        ----
        user_id (str): The Username of the account holder.

        Returns:
        ----
        (dict): All the user accounts.
        """
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"marketdata/barcharts/{symbol}")

        # define the arguments
        params = {
            "access_token": self._access_token,
            "interval": interval,
            "unit": unit,
            "barsback": barsback,
            "firstdate": firstdate,
            "lastdate": lastdate,
            "sessiontemplate": sessiontemplate,
        }

        return self._get_request(url=url_endpoint, params=params)

    def get_crypto_symbol_names(self) -> Response | Awaitable[Response]:
        """Fetch all crypto Symbol Names information."""
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint(url='marketdata/symbollists/cryptopairs/symbolnames"')

        # define the arguments
        params = {"access_token": self._access_token}

        return self._get_request(url=url_endpoint, params=params)

    def get_symbol_details(self, symbols: list[str]) -> Response | Awaitable[Response]:
        """Grabs the info for a particular symbol.

        Arguments:
        ----
        symbol (str): A ticker symbol.

        Raises:
        ----
        ValueError: If no symbol is provided will raise an error.

        Returns:
        ----
        dict: A dictionary containing the symbol info.
        """
        # validate the token.
        self._token_validation()

        if symbols is None:
            raise ValueError("You must pass through a symbol.")
        elif 0 > len(symbols) > 50:
            raise ValueError("You may only send [1..50] symbols per request.")

        # define the endpoint.
        url_endpoint = self._api_endpoint(f'marketdata/symbols/{",".join(symbols)}')

        # define the arguments.
        params = {"access_token": self._access_token}

        return self._get_request(url=url_endpoint, params=params)

    def get_option_expirations(
        self, underlying: str, strike_price: Optional[float] = None
    ) -> Response | Awaitable[Response]:
        """Get the available option contract expiration dates for the underlying symbol.

        Args:
            underlying (str): The symbol for the underlying security on which the option contracts are based.
                The underlying symbol must be an equity or index.
            strike_price (Optional[float], optional): Strike price. If provided,
                only expirations for that strike price will be returned. Defaults to None.
        """
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"marketdata/options/expirations/{underlying}")

        # define the arguments
        params = {"access_token": self._access_token, "strikePrice": strike_price}

        return self._get_request(url=url_endpoint, params=params)

    def get_option_risk_reward(self, price: float, legs: list[dict[str, Any]]) -> Response | Awaitable[Response]:
        """Analyze the risk vs. reward of a potential option trade.

        This endpoint is not applicable for option spread types with different expirations,
        such as Calendar and Diagonal.

        Args:
            price (float): The quoted price for the option spread trade.
            legs (list[dict[str, Any]]): The legs of the option spread trade.
                If more than one leg is specified, the expiration dates must all be the same.
                In addition, leg symbols must be of type stock, stock option, or index option.

        Example Usage:
        ```
        legs = [
                {
                    "Symbol": "string",
                    "Quantity": 0,
                    "TradeAction": "BUY"
                }
            ]

        client = get_option_risk_reward(4.20, legs)
        ```
        """
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint("marketdata/options/riskreward")

        # define the arguments
        params = {
            "access_token": self._access_token,
        }

        payload = {"SpreadPrice": price, "Legs": legs}

        return self._post_request(url=url_endpoint, params=params, data=payload)

    def get_option_spread_types(self) -> Response | Awaitable[Response]:
        """Get the available spread types for option chains."""
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint("marketdata/options/spreadtypes")

        # define the arguments
        params = {
            "access_token": self._access_token,
        }

        return self._get_request(url=url_endpoint, params=params)

    def get_option_strikes(
        self,
        underlying: str,
        spreadType: Optional[str] = None,
        strikeInterval: Optional[int] = None,
        expiration: Optional[datetime] = None,
        expiration2: Optional[datetime] = None,
    ) -> Response | Awaitable[Response]:
        """Get the available strike prices for a spread type and expiration date.

        Args:
            underlying (str): The symbol for the underlying security on which the option contracts are based.
                The underlying symbol must be an equity or index.
            spreadType (Optional[str], optional): The name of the spread type to get the strikes for.
                This value can be obtained from the Get Option Spread Types endpoint.. Defaults to None.
            strikeInterval (Optional[int], optional): Specifies the desired interval between the strike prices in a spread.
                It must be greater than or equal to 1. A value of 1 uses consecutive strikes;
                a value of 2 skips one between strikes; and so on. Defaults to None.
            expiration (Optional[datetime], optional): Date on which the option contract expires; must be a valid expiration date.
                Defaults to the next contract expiration date.. Defaults to None.
            expiration2 (Optional[datetime], optional): Second contract expiration date required for
                Calendar and Diagonal spreads. Defaults to None.
        """
        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint("marketdata/options/strikes/{underlying}")

        # define the arguments
        params = {
            "access_token": self._access_token,
        }

        if spreadType:
            params["spreadType"] = spreadType
        if strikeInterval:
            params["strikeInterval"] = str(strikeInterval)
        if expiration:
            params["expiration"] = expiration.strftime("%m-%d-%Y")
        if expiration2:
            params["expiration2"] = expiration2.strftime("%m-%d-%Y")

        return self._get_request(url=url_endpoint, params=params)

    def get_quote_snapshots(self, symbols: list[str]) -> Response | Awaitable[Response]:
        """Fetch a full snapshot of the latest Quote for the given Symbols.

        For realtime Quote updates, users should use the Quote Stream endpoint.

        Args:
            symbols (list[str]): List of valid symbols. No more than 100 symbols per request.

        Raises:
            ValueError: A minimum of 1 and no more than 100 symbols per request.
        """
        # validate parameters
        if 0 > len(symbols) > 100:
            raise ValueError("A minimum of 1 and no more than 100 symbols per request.")
        else:
            symbols_str = ",".join(symbols)

        # validate the token.
        self._token_validation()

        # define the endpoint.
        url_endpoint = self._api_endpoint(f"marketdata/quotes/{symbols_str}")

        # define the arguments
        params = {
            "access_token": self._access_token,
        }

        return self._get_request(url=url_endpoint, params=params)
